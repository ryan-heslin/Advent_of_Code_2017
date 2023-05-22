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

function is_number(x) {
    return /-?\d+/.test(x);

}

function is_composite(x) {
    if (x % 2 == 0 || x % 3 == 0) return true;
    let stop = Math.ceil(Math.sqrt(x));
    let divisor = 6;
    while (divisor - 1 < stop) {
        if (x % (divisor - 1) == 0 || x % (divisor + 1) == 0) return true;
        divisor += 6;
    }
    return false;


}


const functions = { "set": set, "sub": sub, "mul": mul, "jnz": jnz }

function to_function(parts) {
    let first = parts[1];
    let second = parts[2];
    let second_number = is_number(second);
    if (second_number) { second = Number(second) };
    if (parts[0] == "set") {
        if (second_number) {
            return function(i) {
                registers[first] = second;
                return i + 1;
            }
        } else {
            return function(i) {
                registers[first] = registers[second];
                return i + 1;
            }
        }

    } else if (parts[0] == "mul") {
        if (second_number) {
            return function(i) {
                registers[first] *= second;
                return i + 1;
            }
        } else {
            return function(i) {
                registers[first] *= registers[second];
                return i + 1;
            }
        }
    } else if (parts[0] == "sub") {
        if (second_number) {
            return function(i) {
                registers[first] -= second;
                return i + 1;
            }
        } else {
            return function(i) {
                registers[first] -= registers[second];
                return i + 1;
            }
        }
    } else {
        let first_number = is_number(first);
        if (first_number) {
            first = Number(first);
        }
        // Second jump arg always constant
        if (first_number) {
            if (first == 0) {
                return function(i) { return i + 1 }
            } else {
                return function(i) { return i + second }
            }
        } else {
            return function(i) { return i + (registers[first] == 0 ? 1 : second) }
        }
    }
}

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

j = 0;
let optimized_instructions = instructions.map(to_function);
const stop = optimized_instructions.length;

// I presume this finds the relevant jump line for all inputs
let index = stop;
let found = 0;
while (found < 5) {
    index -= 1
    found += (instructions[index][0] == "jnz")
}
let target_line = index;

while (j != target_line) {
    j = optimized_instructions[j](j);
}

const lower = registers["b"];
const upper = registers["c"];
let step = instructions[stop - 2][2];
let composites = 0;
let current = upper;

while (current >= lower) {
    composites += is_composite(current);
    current += step;
}
console.log(composites);
