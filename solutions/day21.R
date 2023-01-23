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
    hash <- hash_matrix(target)
    mapping[[hash]] <- result
    # Constant matrix, no need for rotations
    if (sum(target) == prod(dim(target))) {
        return()
    }


    for (i in seq_len(4)) {
        hflipped <- hflip(target)
        if (isTRUE(mapping[[hash_matrix(target)]] != result)) stop()
        mapping[[hash_matrix(hflipped)]] <- result
        vflipped <- vflip(target)
        if (isTRUE(mapping[[hash_matrix(target)]] != result)) stop()
        mapping[[hash_matrix(vflipped)]] <- result
        target <- rotate_90(target)
        if (isTRUE(mapping[[hash_matrix(target)]] != result)) stop()
        mapping[[hash_matrix(target)]] <- result
    }
}

expand <- function(start, iterations, mapping) {
    for (i in seq_len(iterations)) {
        # browser()
        extent <- nrow(start)
        dimension <- 2 + (extent %% 3 == 0)
        increment <- dimension - 1
        sequence <- seq(from = 1, to = extent - dimension + 1, by = dimension)
        print(sequence)

        browser()
        temp <- lapply(sequence, \(i){
            rows <- i:(i + increment)
            lapply(
                sequence,
                \(j) mapping[[hash_matrix(start[rows, j:(j + increment)])]]
            )
        })
        print(temp)
        start <- temp |>
            lapply(do.call, what = cbind) |>
            do.call(what = rbind)
        print(start)
    }
    start
}

raw_input <- readLines("inputs/day21.txt")
seed <- ".#.
..#
###"
processed <- strsplit(raw_input, "\\s=>\\s") |>
    lapply(parse_line)
processed

mapping <- new.env()
lapply(processed, map_transforms, mapping = mapping)
start <-
    gsub("(?<=.)\\n?(?=.)", ",", seed, perl = TRUE) |>
    gsub(pattern = "\\.", replacement = "0") |>
    gsub(pattern = "#", replacement = "1") |>
    strsplit(",") |>
    unlist(recursive = FALSE, use.names = FALSE) |>
    strtoi() |>
    matrix(byrow = TRUE, nrow = sqrt(nchar(gsub("\\n", "", seed))))

result <- expand(start, 5, mapping)
part1 <- sum(result)
print(part1)
# 145 too low
