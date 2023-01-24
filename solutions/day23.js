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
registers["a"] = 1;

while (j < instructions.length) {
    args = instructions[j];
    j = functions[args[0]](args[1], args[2], j);
    console.log(registers);
}
console.log(registers["h"]);
