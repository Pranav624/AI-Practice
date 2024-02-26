import time

def minimax(board, turn, ai, depth, alpha, beta, maximizing_player):
    if depth == 0 or end_test(board):
        new_board = final_captures(board)
        return (0, heuristic(new_board, ai))
    moves = possible_moves(board, turn)
    if maximizing_player:
        value = -9999
        best_move = 0
        for move in moves:
            new_board, extra_turn = make_move(board, turn, move)
            if extra_turn:
                new_value = minimax(new_board, turn, ai, depth - 1, alpha, beta, True)[1]
            else:
                new_value = minimax(new_board, -turn, ai, depth - 1, alpha, beta, False)[1]
            if new_value > value:
                value = new_value
                best_move = move
            if value > beta:
                break
            alpha = max(alpha, value)
        return (best_move, value)
    else:
        value = 9999
        best_move = 0
        for move in moves:
            new_board, extra_turn = make_move(board, turn, move)
            if extra_turn:
                new_value = minimax(new_board, turn, ai, depth - 1, alpha, beta, False)[1]
            else:
                new_value = minimax(new_board, -turn, ai, depth - 1, alpha, beta, True)[1]
            if new_value < value:
                value = new_value
                best_move = move
            if value < alpha:
                break
            beta = min(beta, value)
        return (best_move, value)

def heuristic(board, turn):
    return turn * (board[1][6] - board[0][0])

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
    final = (0, 0)
    if turn == 1:
        # Stores val and updates that spot to 0
        val = new_board[1][move - 1]
        if val == 0:
            raise ValueError
        new_board[1][move - 1] = 0

        # Makes the move
        direction = 1
        i = move
        row = 1
        while val > 0:
            if row == 0 and i == 0:
                row = 1
                direction = -direction
                continue
            new_board[row][i] += 1
            final = (row, i)
            if row == 1 and i == 6:
                row = 0
                direction = -direction
            else:
                i += direction
            val -= 1

        # Checks if the final spot was initially empty (now == 1), so it can capture opponent pieces
        if final[0] == 1 and final[1] != 6 and new_board[final[0]][final[1]] == 1:
            new_board[1][6] += new_board[0][final[1] + 1]
            new_board[0][final[1] + 1] = 0
    else:
        val = new_board[0][move]
        if val == 0:
            raise ValueError
        new_board[0][move] = 0
        
        direction = -1
        i = move - 1
        row = 0
        while val > 0:
            if row == 1 and i == 6:
                row = 0
                direction = -direction
                continue
            new_board[row][i] += 1
            final = (row, i)
            if row == 0 and i == 0:
                row = 1
                direction = -direction
            else:
                i += direction
            val -= 1

        if final[0] == 0 and final[1] != 0 and new_board[final[0]][final[1]] == 1:
            new_board[0][0] += new_board[1][final[1] - 1]
            new_board[1][final[1] - 1] = 0

    extra_turn = False
    if (final == (1, 6) and turn == 1) or (final == (0, 0) and turn == -1):
        extra_turn = True
    return (new_board, extra_turn)

def final_captures(board):
    new_board = [row[:] for row in board]
    if 0 == board[0][1] == board[0][2] == board[0][3] == board[0][4] == board[0][5] == board[0][6]:
        new_board[1][6] += board[1][0] + board[1][1] + board[1][2] + board[1][3] + board[1][4] + board[1][5]
        new_board[1][0] = new_board[1][1] = new_board[1][2] = new_board[1][3] = new_board[1][4] = new_board[1][5] = 0
    else:
        new_board[0][0] += board[0][1] + board[0][2] + board[0][3] + board[0][4] + board[0][5] + board[0][6]
        new_board[0][1] = new_board[0][2] = new_board[0][3] = new_board[0][4] = new_board[0][5] = new_board[0][6] = 0
    return new_board

def end_test(board):
    if 0 == board[0][1] == board[0][2] == board[0][3] == board[0][4] == board[0][5] == board[0][6] or \
       0 == board[1][0] == board[1][1] == board[1][2] == board[1][3] == board[1][4] == board[1][5]:
        return True
    return False

def display(board):
    output = f'  {board[0][1]} {board[0][2]} {board[0][3]} {board[0][4]} {board[0][5]} {board[0][6]}\n'
    output += f'{board[0][0]}             {board[1][6]}\n'
    output += f'  {board[1][0]} {board[1][1]} {board[1][2]} {board[1][3]} {board[1][4]} {board[1][5]}\n'
    return output

def main():
    ai = int(input("Is AI 1 or 2? "))
    if ai == 2:
        ai = -1
    board = [[4 for _ in range(7)] for _ in range(2)]
    player = {1: 'Player 1', -1: 'Player 2'}
    board[0][0] = 0
    board[1][6] = 0
    print(display(board))

    turn = 1
    depth = 10

    while end_test(board) == False:
        if turn != ai:
            print("Possible Moves:", possible_moves(board, turn))
            move = int(input(f"{player[turn]}'s turn. What is your move? "))
            try:
                new_board, extra_turn = make_move(board, turn, move)
            except:
                print("That spot is already empty.\n")
                continue
        else:
            t = time.time()
            move = minimax(board, turn, ai, depth, -9999, 9999, True)[0]
            new_board, extra_turn = make_move(board, turn, move)
            print(f"Bot ({ai}) played {move} in {time.time() - t} seconds.")

        board = new_board
        print(display(board))
        if not extra_turn:
            turn = -turn

    new_board = final_captures(board)
    print("Final Board")
    print(display(new_board))
    if new_board[0][0] < new_board[1][6]:
        print("Player 1 won!")
    elif new_board[0][0] > new_board[1][6]:
        print("Player 2 won!")
    else:
        print("It's a tie!")

if __name__ == '__main__':
    main()