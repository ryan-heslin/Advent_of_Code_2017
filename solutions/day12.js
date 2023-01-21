function parse_line(line){
    let parts = line.split(" <-> ");
    parts[1] = parts[1].split(", ");
    return parts;
}

function count(parent, groups){
    let children = new Set();
    function helper(id){
        let ids = groups[id];
        children.add(id);

        for(child of ids){
            if(!(children.has(child))){
                helper(child);
            }
        }
    }
    helper(parent);

    return children;
}

function count_groups(groups, target){
    let visited = new Set();
    let found = 0;
    let part1 = NaN;
    for(key of Object.keys(groups)){
        if(!(visited.has(key))){
            let new_group = count(key, groups);
            if(key == target){
                part1 = new_group.size;
            }
            visited = new Set([...visited, ...new_group]);
            found ++;
        }
    }
    return [part1, found];
}



const fs = require('fs');
const raw_input = fs.readFileSync('inputs/day12.txt', 'utf-8').toString().split("\n");
raw_input.pop();
const groups = Object.fromEntries(raw_input.map(parse_line));

const id = "0";
const result = count_groups(groups, id);
const part1 = result[0];
console.log(part1);

const part2 = result[1];
console.log(part2);
