#!/usr/bin/python3

from z3 import *
import argparse
import csv

def read_level(filename):
    # Open the file
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                # int_row = [int(item) if item is not "" else -1 for item in row]  # Convert each item in the row to an integer
                int_row = [-1 if item.strip() == "" or item == " " or item == "\t" else int(item) for item in row]  # Convert each item in the row to an integer
                data.append(int_row)
            return data
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        exit(-1)

def handle_args():
    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle using Z3 solver.")
    parser.add_argument("file", type=str, help="Path to the input file")

    # Parse command-line arguments
    return parser.parse_args()

def get_neighbors(matrix, row, col):
    # List of relative positions of the 8 neighbors
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
        ( 0, -1), (0, 0) , ( 0, 1),   # Left, Self, Right
        ( 1, -1), ( 1, 0), ( 1, 1)    # Bottom-left, Bottom, Bottom-right
    ]
    
    # List to store valid neighbors
    valid_neighbors = []
    
    # Iterate over each relative position
    for dr, dc in neighbors:
        new_row, new_col = row + dr, col + dc
        
        # Check if the new position is within bounds of the matrix
        if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
            valid_neighbors.append(matrix[new_row][new_col])
    
    return valid_neighbors

def add_sudoku_constraint(solver: Solver, vars):
    and_list = []
    for constant in range(1,10):
        or_list = []
        for i in range(9):
            or_list.append(constant == vars[i])
        and_list.append(Or(or_list))
    solver.add(And(and_list))

def solve_level(level):
    solver = Solver()
    level_size = 9
    vars = [[Int(f"var_{i}_{o}") for i in range(level_size)] for o in range(level_size)]

    # add constant constraints
    for row_index, row in enumerate(level):
        for column_index, square in enumerate(row):
            if square == -1:
                continue
            solver.add(vars[row_index][column_index] == square)

    # add row constraints
    for row_index, row in enumerate(level):
        add_sudoku_constraint(solver, vars[row_index])

    # add column constraints
    for i in range(9):
        column = [row[i] for row in vars]
        add_sudoku_constraint(solver, column)

    # add square contraints
    for r in range(3):
        for c in range(3):
            square = get_neighbors(vars, 3 * r + 1, 3 * c + 1)
            add_sudoku_constraint(solver, square)

    # Check satisfiability
    if solver.check() == sat:
        model = solver.model()
        return [[model[square] for square in row] for row in vars]  # Return the values of the variables
    else:
        print("No solution exists")
        exit(-1)

def main():
    args = handle_args()

    level = read_level(args.file)
    if len(level) != 9:
        print("Invalid level size of " + str(len(level)))
        exit(-1)

    for row in level:
        for square in row:
            print(square if square != -1 else " ", end=" ")
        print()

    print()
    
    solution = solve_level(level)
    for row in solution:
        for square in row:
            print(square, end=" ")
        print()

if __name__ == "__main__":
    main()