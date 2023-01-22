const fs = require('fs');

function parse(line) {
    return line.split(": ").map(Number);
}

function severity(layer) {
    depth = Number(layer[0]);
    // Has to visit each square but end twice
    return (depth % (((layer[1] - 1) * 2)) == 0) * depth * layer[1];
}

function compute() {
    return Object.entries(mapping).map(severity).reduce((x, y) => x + y);
}

function test(wait) {
    for (k of Object.keys(mapping)) {
        if ((wait + Number(k)) % ((mapping[k] - 1) * 2) == 0) {
            return false;
        }
    }
    return true;

}

const raw_input = fs.readFileSync('inputs/day13.txt', 'utf-8').toString().split("\n");
raw_input.pop();
const mapping = Object.fromEntries(raw_input.map(parse));

const part1 = compute();
let result = false;
let part2 = 0;
console.log(part1)
while (!result) {
    part2++;
    result = test(part2);
}

console.log(part2);
