const weights = {};
const total_weights = {};
const carried = {};


function weigh(node){
    let children = carried[node];
    let own_weight = weights[node];
    if(children.length == 1){
        total_weights[node] = weights[node];
        return own_weight;
    }
    //console.log(children.forEach(weigh));
    own_weight += children.map(weigh).reduce((x, y) => x + y);
    total_weights[node] = own_weight;
    return own_weight;
}

function balance(node, sibling_weight){
    let children = carried[node];
    let result = 0;
    if(children.length <= 1){
        return result;
    }

    let these_weights = children.map((x) => total_weights[x]);
    let max_weight = Math.max(...these_weights);
    let min_weight = Math.min(...these_weights);

    if (min_weight != max_weight){
        weights_count = {};
        for(child of children){
            if(!(total_weights[child] in weights_count)){
                weights_count[total_weights[child]] = [];
            }
            weights_count[total_weights[child]].push(child);

        }
        if(children.length > 2){
            // Only one out of balance
            let imbalanced = Object.entries(weights_count).filter((x) => x[1].length == 1);
            let balanced_weight = Number(Object.keys(weights_count).filter((x) => weights_count[x].length > 1));
            let imbalanced_program = imbalanced[0][1];
            result = balance(imbalanced_program, balanced_weight);
            if( result == 0){
                console.log(Number(imbalanced[0][0]))
                console.log(these_weights);
                result = weights[imbalanced_program] -( Number(imbalanced[0][0]) - balanced_weight);
            }
            return result;

        // If two children, rebalance the one that makes this node weigh the same as its siblings
        }else{
            // I hope this is accurate for the case where the imbalanced program
            // is one of two
            let first = children[0];
            let second = children[1];
            result = balance(first, total_weights[second]);
            if(result ==0){
                result = balance(second, total_weights[first]);
                if(result == 0){
                    let candidate = weights[first] - (total_weights[first] - total_weights[second]);
                    if(sibling_weight == 0 || candidate + (total_weights[first] - weights[first]) == sibling_weight ){
                        return candidate;
                    }
                    return weights[second] - (total_weights[second] - total_weights[first]);
                }
                return result;
            }
            return result;

        }
    }
    //Perfectly balanced, as all things should be
    for(child of children){
        result = balance(child, max_weight);
        if(result > 0){
            break
        }
    }
    return result;

    }

const children = new Set();
const fs = require('fs');
const raw_input = fs.readFileSync('inputs/day7.txt', 'utf-8').toString().split("\n");

for(let line of raw_input){
    line = line.replace(/[()]/, "");
    let parts =  line.split(/[^a-z0-9]+/);
    name = parts[0];
    weights[name] = Number(parts[1]);
    carried[name] = parts.slice(2);
    parts.slice(2).forEach(x => children.add(x));
}

let part1  = Object.keys(carried).filter(program => !(children.has(program)))[0];
console.log(part1);

weigh(part1);

const part2 = balance(part1, 0);
console.log(part2);
