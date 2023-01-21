function parse(line){
    return line.split(": ").map(Number);
}

function severity(layer,wait = 0, count_zero = false){
    depth = Number(layer[0]);
    // Has to visit each square but end twice
 return  ( (wait + depth) % (((layer[1] -1) * 2)) == 0) * Math.max(depth, Number(count_zero)) * layer[1];
}

function compute(wait, ignore_zero = true){
    return Object.entries(mapping).map((x) => severity(x, wait = wait, ignore_zero = ignore_zero)).reduce((x, y) => x + y);
}

const fs = require('fs');
const raw_input = fs.readFileSync('inputs/day13.txt', 'utf-8').toString().split("\n");
raw_input.pop();
const mapping = Object.fromEntries(raw_input.map(parse));

const part1 = compute(0, false);
let result = 1000;
let part2 = 0;
console.log(part1)
while(result >0){
    part2 ++;
    result = compute(part2, true);
}

console.log(part2);
