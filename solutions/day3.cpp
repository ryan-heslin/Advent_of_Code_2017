#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

pair<int, int> find_start(int target){
   int this_start = 2;
   int old_start;
   int this_side = 1;
   int old_side;
   while (this_start < target){
       old_start = this_start;
       old_side = this_side;
       this_side = old_side + 2;
       this_start += ((this_side - 1) * 4);
   }
   return  {old_start, this_side};
}

int find_distance(int start,  int side_length, int target){
    int step = -1;
    int top = floor(side_length / 2);
    int current = top - 1;
    int bottom = 0;
    for(int i = start; i <= start + (side_length - 1) * 4; i++){
        if (i == target){
            return top + current;
        }
        if (current == top){
            step = -1;
        }else if(current == bottom){
            step = 1;
        }
        current += step;
    }
}

int solve_part2(int target){

    int size = floor(ceil(sqrt(target)) / 2);
    int numbers[size][size] = {0};
    int center = floor(size / 2);
    int x = center;
    int y = center;
    int current = 1;
    numbers[center][center] = current;
    int current_side = 1;
    int half;
    int imax;
    int imin;
    int left;
    int below;
    int right;
    int above;

    while(true){
        current_side += 2;
        half = floor(current_side /2);
        imin = center - half;
        imax = center + half;
        //One-time adjustment
        x ++;
        y --;
        // Left; ignore right and above
        left = x -1;

        while( y < imax){
            y ++;
            current = numbers[y-1][x] + numbers[y-1][left] + numbers[y][left]
                + numbers[y+1][left];
            if (current > target){
                return current;

            }
            numbers[y][x] = current;

        }

        // Top
        below = y-1;
        while(x > imin){
                    x--;
                    current = numbers[y][x+1] + numbers[below][x-1] + numbers[below][x]
                        + numbers[below][x+1];
                    if (current > target){
                        return current;

                    }
                    numbers[y][x] = current;
                    }

        // Right
        right = x + 1;
        while(y > imin){
                    y--;
                    current = numbers[y+1][x] + numbers[y-1][right] + numbers[y][right]
                        + numbers[y+1][right];
                    if (current > target){
                        return current;

                    }
                    numbers[y][x] = current;
                    }
        // Bottom
        above = y + 1;
        while(x < imax){
                    x++;
                    current = numbers[y][x-1] + numbers[above][x-1] + numbers[above][x]
                        + numbers[above][x+1];
                    if (current > target){
                        return current;

                    }
                    numbers[y][x] = current;
                    }
    }

}

int  main(){
int target = 277678;
pair<int , int> result = find_start(target);
//cout << result.first << "\n" << result.second << "\n";
int part1 = find_distance(result.first, result.second, target);
cout << part1 << "\n";

int part2 = solve_part2(target);
cout << part2 << "\n";
return 0;
}
