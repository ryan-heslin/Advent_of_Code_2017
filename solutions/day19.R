library(magrittr)

index2coords <- function(X, index) {
    c(
        ifelse(index %% nrow(X) == 0, nrow(X), index %% nrow(X)),
        index %% ncol(X) + 1
    )
}
coords2index <- function(X, coords) {
    coords[1] + nrow(X) * coords[2]
}

next_direction <- function(input, coords, last_dir, passed, steps) {
    candidates <- surrounds(input, coords)
    excludes <- c(
        l = "r",
        r = "l",
        u = "d",
        d = "u"
    )
    candidates <-
        candidates[rownames(candidates) != excludes[last_dir], ]
    next_dir <-
        rownames(candidates[input[candidates] != " ", , drop = FALSE])
    print(coords)
    traverse(input,
        coords,
        dir = next_dir,
        passed = passed,
        steps = steps
    )
}
surrounds <- function(input, coords) {
    base <- c(1, -1, 0, 0)
    adds <- cbind(base, rev(base))
    out <- sweep(adds,
        FUN = `+`,
        STATS = c(coords),
        MARGIN = 2
    )
    rownames(out) <- c("d", "u", "l", "r")
    out[validate_coords(input, coords), ]
}
validate_coords <- function(input, coords) {
    dims <- dim(input)
    apply(coords, MARGIN = 1, function(x) {
        all(x > 0 && x <= dims)
    })
}
traverse <-
    function(input,
             coords,
             dir = c("l", "r", "u", "d"),
             min_ind = 1,
             max_ind = 201,
             passed,
             steps) {
        reverse <- if (dir %in% c("l", "u")) {
            -1
        } else {
            1
        }
        stop_ind <- ifelse(dir %in% c("l", "u"), min_ind, max_ind)
        if (dir %in% c("l", "r")) {
            subscript <- cbind(coords[1], seq(coords[2] + reverse, stop_ind))
        } else {
            subscript <- cbind(seq(coords[1] + reverse, stop_ind), coords[2])
        }
        # Get closest + - next turning point
        if (grepl("(?:\\||-)[A-Z]\\s", paste(input[subscript], collapse = ""))) {
            traversed <- input[subscript]
            steps <- steps + which(traversed %in% LETTERS) + 1
            return(list(
                part1 = c(passed, traversed[traversed %in% LETTERS]),
                part2 = steps
            ))
        }
        cells_traversed <- which(input[subscript] == "+")[1]
        steps <- steps + cells_traversed
        # Return if no + on line - must mean last row-column
        coords <- subscript[cells_traversed, , drop = FALSE]
        traversed <- input[subscript[1:cells_traversed, ]]
        passed <-
            c(passed, traversed[traversed %in% LETTERS])
        next_direction(input, coords, last_dir = dir, passed, steps = steps)
    }

start_row <- 1L
input <- readLines("inputs/day19.txt") |>
    sapply(strsplit, "", USE.NAMES = FALSE) |>
    simplify2array() |>
    t() |>
    as.matrix()

start <- c(1, which(input[1, ] != " "))

traverse(input,
    start,
    dir = "d",
    passed = character(),
    steps = 0
)
