const fs = require('fs');

const divisor = 2147483647;
const modulus = 2 ** 16;

function solve(a, b) {
    let matches = 0;
    let part2_length = 5000000
    let i = 0;
    let as = [];
    let bs = [];

    while ((i < 40000000) || ((as.length < part2_length) || (bs.length < part2_length))) {
        a["number"] *= a["factor"];
        b["number"] *= b["factor"];
        a["number"] %= divisor;
        b["number"] %= divisor;
        matches += (i < 40000000 && a["number"] % modulus == b["number"] % modulus);

        if (as.length < part2_length && (a["number"] % 4 == 0)) {
            as.push(a["number"]);
        }
        if (bs.length < part2_length && (b["number"] % 8 == 0)) {
            bs.push(b["number"]);
        }
        i++;
    }
    let part2 = as.map((x, i) => x % modulus == bs[i] % modulus).reduce((x, y) => x + y);

    return [matches, part2];
}

const raw_input = fs.readFileSync('inputs/day15.txt', 'utf-8').toString();
const generators = raw_input.split("\n").map((x) => Number(x.match(/\d+/)));
let a = { "number": generators[0], "factor": 16807 }
let b = { "number": generators[1], "factor": 48271 }

const answer = solve(a, b);
console.log(answer[0]);
console.log(answer[1]);
