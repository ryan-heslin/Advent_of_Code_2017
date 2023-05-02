parse_line <- function(parts) {
    nrows <- gsub("/", "", parts) |>
        nchar() |>
        sqrt()

    parts <- gsub("(?<=.)/?(?=.)", ",", parts, perl = TRUE) |>
        gsub(pattern = "\\.", replacement = "0") |>
        gsub(pattern = "#", replacement = "1") |>
        strsplit(",") |>
        lapply(strtoi)

    parts[[1]] <- matrix(parts[[1]], nrow = nrows[[1]], byrow = TRUE)
    parts[[2]] <- matrix(parts[[2]], nrow = nrows[[2]], byrow = TRUE)
    parts
}

hash_matrix <- function(x) {
    paste(x, collapse = ",")
}

# Over vertical line
hflip <- function(x) {
    x[, seq(ncol(x), 1)]
}

# Over horizontal line
vflip <- function(x) {
    x[seq(nrow(x), 1), ]
}

# https://stackoverflow.com/questions/16496210/rotate-a-matrix-in-r-by-90-degrees-clockwise
rotate_90 <- function(x) {
    apply(x, 2, rev) |>
        t()
}

map_transforms <- function(pair, mapping) {
    target <- pair[[1]]
    result <- pair[[2]]
    # Constant matrix, no need for rotations
    if (length(unique(target)) == 1) {
        hash <- hash_matrix(target)
        mapping[[hash]] <- result
        return()
    }


    for (i in seq_len(4)) {
        hflipped <- hflip(target)
        mapping[[hash_matrix(hflipped)]] <- result
        vflipped <- vflip(target)
        mapping[[hash_matrix(vflipped)]] <- result
        target <- rotate_90(target)
        mapping[[hash_matrix(target)]] <- result
    }
}

expand <- function(start, iterations, mapping) {
    for (i in seq_len(iterations)) {
        extent <- nrow(start)
        dimension <- if (extent %% 2 == 0) 2 else 3
        increment <- dimension - 1
        sequence <- seq(from = 1, to = extent - dimension + 1, by = dimension)

        start <- lapply(sequence, \(i){
            rows <- i:(i + increment)
            lapply(
                sequence,
                \(j) mapping[[hash_matrix(start[rows, j:(j + increment)])]]
            )
        }) |>
            lapply(do.call, what = cbind) |>
            do.call(what = rbind)
    }
    start
}

raw_input <- readLines("inputs/day21.txt")
seed <- ".#.
..#
###"
processed <- strsplit(raw_input, "\\s=>\\s") |>
    lapply(parse_line)

mapping <- new.env()
invisible(lapply(processed, map_transforms, mapping = mapping))
start <-
    gsub("(?<=.)\\n?(?=.)", ",", seed, perl = TRUE) |>
    gsub(pattern = "\\.", replacement = "0") |>
    gsub(pattern = "#", replacement = "1") |>
    strsplit(",") |>
    unlist(recursive = FALSE, use.names = FALSE) |>
    strtoi() |>
    matrix(byrow = TRUE, nrow = sqrt(nchar(gsub("\\n", "", seed))))

part1_iterations <- 5
part2_iterations <- 18
result <- expand(start, part1_iterations, mapping)
part1 <- sum(result)

result <- expand(result, part2_iterations - part1_iterations, mapping)
part2 <- sum(result)
print(part1)
part2 <- sum(result)
print(part2)
