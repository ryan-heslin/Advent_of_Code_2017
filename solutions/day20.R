parse_line <- function(line, dimnames, nrow) {
    gsub("[<>a-z=]", "", line) |>
        strsplit(",") |>
        unlist(use.names = FALSE, recursive = FALSE) |>
        strtoi() |>
        matrix(nrow = nrow, dimnames = dimnames)
}

minimize <- function(data, iterations) {
    prev <- sum(abs(data[, "p"]))
    m <- nrow(data)
    n <- ncol(data)


    multiplier <- c(1, iterations, choose(iterations + 1, 2))
    result <- data %*% diag(multiplier)
    .rowSums(result, m = m, n = n) |>
        abs() |>
        sum()
}

simulate <- function(particles, iterations) {
    streak <- 0
    old <- nrow(particles)
    for (i in seq_len(iterations)) {
        sequence <- seq_len(nrow(particles))
        for (j in sequence) {
            particles[, "v"][[j]] <- particles[, "v"][[j]] + particles[, "a"][[j]]
            particles[, "p"][[j]] <- particles[, "p"][[j]] + particles[, "v"][[j]]
        }
        hashes <- vapply(particles[, "p"],
            \(x) paste(x, collapse = ","),
            FUN.VALUE = character(1)
        )
        counts <- table(hashes)
        duplicates <- names(counts[counts > 1])
        particles <- particles[!hashes %in% duplicates, ]
        new <- nrow(particles)
        if (new != old) {
            streak <- 0
        } else {
            streak <- streak + 1
        }
        if (streak > 100) break
        old <- new
    }
    nrow(particles)
}



raw_input <- readLines("inputs/day20.txt")

vectors <- strsplit(raw_input, ",\\s")
dimnames <- list(c("x", "y", "z"), substr(vectors[[1]], 1, 1))
nrow <- length(dimnames[[1]])
vectors <- lapply(vectors, parse_line, dimnames = dimnames, nrow = nrow)

iterations <- max(abs(unlist(vectors)))
results <- vapply(vectors, minimize, FUN.VALUE = numeric(1), iterations = iterations)
part1 <- which.min(results) - 1
print(part1)

vectors <- lapply(vectors, asplit, MARGIN = 2) |> do.call(what = rbind)
part2 <- simulate(vectors, iterations = iterations) |>
    suppressWarnings()
print(part2)
