# Sudoku Solver

a solver for the popular puzzle game Sudoku.
This solver utilizes the z3 SAT-solver

## Usage

```bash
./main.py levels/test_hard_1.csv
```

Output:

```
Detected level size: 15x15
3         9 1 4   
1   2 7           
7       5     2   
8       7     5   
    3 1   4 7     
  9     3       1 
  5     9       6 
          8 5   2 
  7 1 2           

3 6 5 8 2 9 1 4 7 
1 4 2 7 6 3 8 9 5 
7 8 9 4 5 1 6 2 3 
8 1 6 9 7 2 3 5 4 
5 2 3 1 8 4 7 6 9 
4 9 7 5 3 6 2 8 1 
2 5 8 3 9 7 4 1 6 
9 3 4 6 1 8 5 7 2 
6 7 1 2 4 5 9 3 8 
```
