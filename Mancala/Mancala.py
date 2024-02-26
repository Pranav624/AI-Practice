def possible_moves(board, turn):
    moves = []
    if turn == 1:
        for i in range(6):
            if board[1][i] != 0:
                moves.append(i + 1)
    else:
        for i in range(1, 7):
            if board[0][i] != 0:
                moves.append(i)
    return moves

def make_move(board, turn, move):
    new_board = [row[:] for row in board]
    if turn == 1:
        # Makes the move
        val = new_board[1][move - 1]
        new_board[1][move - 1] = 0
        final = (0, 0)
        for i in range(move, move + val):
            row = 1
            index = i
            if i > 6:
                row = 0
                index = -(i - 6)
            new_board[row][index] += 1
            final = (row, index)
        # Checks if the final spot was initially empty (now == 1), so it can capture opponent pieces
        if final[0] == 1 and final[1] != 6 and new_board[final[0]][final[1]] == 1:
            new_board[1][6] += new_board[0][final[1] + 1]
            new_board[0][final[1] + 1] = 0
    else:
        val = new_board[0][move]
        new_board[0][move] = 0
        final = (0, 0)
        for i in range(move - 1, move - val - 1, -1):
            row = 0
            index = i
            if i < 0:
                row = 1
                index = -(i + 1)
            new_board[row][index] += 1
            final = (row, index)
        if final[0] == 0 and final[1] != 0 and new_board[final[0]][final[1]] == 1:
            new_board[0][0] += new_board[1][final[1] - 1]
            new_board[1][final[1] - 1] = 0
    return new_board

def end_test(board):
    if board[0][1] == board[0][2] == board[0][3] == board[0][4] == board[0][5] == board[0][6] == 0 or \
       board[1][0] == board[1][1] == board[1][2] == board[1][3] == board[1][4] == board[1][5] == 0:
        return True
    return False

def display(board):
    output = f'  {board[0][1]} {board[0][2]} {board[0][3]} {board[0][4]} {board[0][5]} {board[0][6]}\n'
    output += f'{board[0][0]}             {board[1][6]}\n'
    output += f'  {board[1][0]} {board[1][1]} {board[1][2]} {board[1][3]} {board[1][4]} {board[1][5]}\n'
    return output

def main():
    board = [[4 for _ in range(7)] for _ in range(2)]
    board[0][0] = 0
    board[1][6] = 0
    print(display(board))

    turn = 1
    while end_test(board) == False:
        print("Possible Moves:", possible_moves(board, turn))
        move = int(input("What is your move? "))
        new_board = make_move(board, turn, move)
        board = new_board
        print(display(board))
        turn = -turn

if __name__ == '__main__':
    main()