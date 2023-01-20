const fs = require('fs');

function solve(state){
    let i = 1;
    let seen = {};
    seen[state.toString()] = 0;
    let size = state.length;

    while(true){
        //https://stackoverflow.com/questions/11301438/return-index-of-greatest-value-in-an-array
        // index of max
        let target = state.reduce((imax, x, i, state) => x > state[imax] ? i : imax, 0);
        let n_blocks = state[target];
        let per_block = Math.floor(n_blocks / size);
        let leftover = n_blocks % size;
        state[target] = 0;

        for(let i=1; i <= size; i++){
            state[(target + i) % size] += per_block + (leftover > 0);
            leftover --;
        }
        let record = state.toString();
        if(record in seen){
            return [i, i - seen[record] ] ;
        }
        seen[record] = i;
        i ++;
    }

    return i;
}

const raw_input = fs.readFileSync('inputs/day6.txt', 'utf-8').toString().replace("\n", "").split("\t");
const state = raw_input.map(Number);
const answer = solve(state);
console.log(answer[0]);
console.log(answer[1]);
