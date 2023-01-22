const fs = require('fs');
const registers = {};

const ops = {
    ">=": function(lhs, rhs) { return lhs >= rhs; },
    ">": function(lhs, rhs) { return lhs > rhs; },
    "<=": function(lhs, rhs) { return lhs <= rhs; },
    "<": function(lhs, rhs) { return lhs < rhs; },
    "!=": function(lhs, rhs) { return lhs != rhs; },
    "==": function(lhs, rhs) {
        return lhs == rhs
            ;
    }
}

function parse(line) {
    let parts = line.split(" ");
    parts[2] = Number(parts[2]);
    parts[6] = Number(parts[6]);
    parts[2] = parts[1] == "inc" ? parts[2] : -parts[2]
    return { "target": parts[0], "addend": parts[2], "comparison": parts[4], "operator": ops[parts[5]], "compare_val": parts[6] }
}
const raw_input = fs.readFileSync('inputs/day8.txt', 'utf-8').toString();
const instructions = raw_input.split("\n").map(parse);
instructions.pop();
let part2 = 0;

for (const line of instructions) {
    if (!(line["target"] in registers)) {
        registers[line["target"]] = 0;
    }
    if (!(line["comparison"] in registers)) {
        registers[line["comparison"]] = 0;
    }

    registers[line["target"]] += line["operator"](registers[line["comparison"]], line["compare_val"]) * line["addend"]
    part2 = Math.max(registers[line["target"]], part2);
}

const part1 = Math.max(...Object.values(registers));
console.log(part1);
console.log(part2);
