#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"
#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):

    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    empty = find_empty(board)
    if not empty:
        return board
    row, col = empty[0], empty[1]

    for num  in range(1,10):
        if valid(board, num, empty):
            board[row + col] = num

            result = backtracking(board)
            if result:
                return result

            board[row + col] = 0
    return None
            
    # TODO: implement this
    solved_board = board
    return solved_board

def find_empty(board):
    for r in ROW:
        for c in COL:
            if board[r + c] == 0:
                return r+c
    return None

def valid(board, num, position):
    row, col = position[0], position[1]


    for c in COL:
        if board[row + c] == num:
            return False
    
    for r in ROW:
        if board[r + col] ==  num:
            return False


    square_x = (ord(row) - ord('A')) // 3 * 3
    square_y = (int(col) - 1) // 3 * 3


    for i in range(square_x, square_x+ 3):
        for j in range(square_y, square_y + 3):
            if board[ROW[i]+COL[j]] == num:
                return False
    
    return True
    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) < 9:
            print("Input string too short")
            exit()

        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
       
   
        solved_board = backtracking(board)
        
    
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    else:
        print("Usage: python3 sudoku.py <input string>")
        exit()
    
    print("Finishing all boards in file.")

