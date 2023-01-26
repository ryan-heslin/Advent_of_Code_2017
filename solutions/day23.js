const fs = require("fs");
let muls = 0;

const ascii_a = 97;
registers = Object.fromEntries([...Array(7).keys()].map((x) => [String.fromCharCode(x + ascii_a), 0]));

function resolve(val) {
    return (val in registers) ? registers[val] : val;
}

function parse_line(line) {
    return line.split(" ").map((x) => /-?\d+/.test(x) ? Number(x) : x)
}

function set(x, y, i) {
    registers[x] = resolve(y);
    return i + 1;
}

function sub(x, y, i) {
    registers[x] -= resolve(y);
    return i + 1;
}

function mul(x, y, i) {
    registers[x] *= resolve(y);
    muls++;
    return i + 1;
}

function jnz(x, y, i) {
    i += (resolve(x) == 0) ? 1 : resolve(y);
    return i;
}


const functions = { "set": set, "sub": sub, "mul": mul, "jnz": jnz }
const raw_input = fs.readFileSync('inputs/day23.txt', 'utf-8').toString().split("\n");
raw_input.pop();
const instructions = raw_input.map(parse_line);

function to_function(line) {
    let func = functions[line[0]]
    if (typeof line[1] === "string" && typeof line[2] === "string") {
        let result = function() { func(registers[line[1]], registers[line[2]]) };
    } else if (typeof line[1] === "string") {
        let result = function() { func(registers[line[1]], line[2]) };
    } else if (typeof line[2] === "string") {
        let result = function() { func(line[1], registers[line[2]]) };
    } else {
        let result = function() { func(line[1], line[2]) };
    }
    return result;
}
instructions = instructions.map(to_function);
let i = 0;
while (i < instructions.length) {
    args = instructions[i];
    i = functions[args[0]](args[1], args[2], i);
}
console.log(muls);

let j = 0;

for (k of Object.keys(registers)) {
    registers[k] = 0;
}
a = 1;

let lines = {};
let counter = 0;
j = 3;
// THe key: sometimes the jnz f 0 clause skips writing to h, so fewer
// than 1000 writes are done.
// Each loop: inc b, g, e 17
// These are values after first loop through 'jnz g -13' instruction
// registers["a"] = 1;
// registers["b"] = 122683;
// registers["c"] = 122700;
// registers["d"] = 105700;
// registers["e"] = 122683;
// registers["f"] = 0;
// registers["g"] = -17;
// registers["h"] = 1;
// Innermost loop is mod test, says subreddit
while (j < instructions.length) {
    counter++;
    args = instructions[j];
    j = functions[args[0]](args[1], args[2], j);
    // if (j == 23) {
    //     console.log(registers);
    //     console.log("\n");
    // }
    if (j == 25) {
        console.log(registers);
    }
}
console.log(registers["h"]);
//1000 too high
