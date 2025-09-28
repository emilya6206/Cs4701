#!/bin/bash

echo "Testing 6,1,8,4,0,2,7,3,5"
echo "----------------------------"
python3 puzzle.py dfs 6,1,8,4,0,2,7,3,5
echo

python3 puzzle.py bfs 6,1,8,4,0,2,7,3,5
echo

python3 puzzle.py ast 6,1,8,4,0,2,7,3,5
echo

echo "Testing 8,6,4,2,1,3,5,7,0"
echo "----------------------------"

python3 puzzle.py dfs 8,6,4,2,1,3,5,7,0

python3 puzzle.py bfs 8,6,4,2,1,3,5,7,0

python3 puzzle.py ast 8,6,4,2,1,3,5,7,0

echo "Testing 8,7,6,5,4,3,2,1,0"
echo "----------------------------"

python3 puzzle.py dfs 8,7,6,5,4,3,2,1,0

python3 puzzle.py bfs 8,7,6,5,4,3,2,1,0

python3 puzzle.py ast 8,7,6,5,4,3,2,1,0







