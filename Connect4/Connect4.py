import time

opp = {'R': 'Y', 'Y': 'R'}
TABLE = {}

def create_win_table():
    table = []
    for r in range(6):
        for c in range(4):
            table.append([(r, c), (r, c+1), (r, c+2), (r, c+3)])
    for r in range(3):
        for c in range(7):
            table.append([(r, c), (r+1, c), (r+2, c), (r+3, c)])
    for r in range(3):
        for c in range(4):
            table.append([(r, c), (r+1, c+1), (r+2, c+2), (r+3, c+3)])
    for r in range(3, 6):
        for c in range(4):
            table.append([(r, c), (r-1, c+1), (r-2, c+2), (r-3, c+3)])
    return table

def minimax(board, turn, ai, win_table, depth, alpha, beta, maximizing_player):
    if depth == 0 or end_test(board, win_table)[0]:
        return (0, heuristic(board, ai, win_table, depth))
    moves = possible_moves(board, turn, win_table)
    if maximizing_player:
        value = -99999999999999
        best_move = 0
        for move in moves:
            new_board = make_move(move, turn, board)
            new_value = minimax(new_board, opp[turn], ai, win_table, depth - 1, alpha, beta, False)[1]
            if new_value > value:
                value = new_value
                best_move = move
            if value > beta:
                break
            alpha = max(alpha, value)
        return (best_move, value)
    else:
        value = 99999999999999
        best_move = 0
        for move in moves:
            new_board = make_move(move, turn, board)
            new_value = minimax(new_board, opp[turn], ai, win_table, depth - 1, alpha, beta, True)[1]
            if new_value < value:
                value = new_value
                best_move = move
            if value < alpha:
                break
            beta = min(beta, value)
        return (best_move, value)

def heuristic(board, turn, win_table, depth):
    score = 0
    multiple_threats = 0
    multiple_blocks = 0

    for i in win_table:
        l = [board[i[j][0]][i[j][1]] for j in range(4)]
        empty_count = l.count('.')
        if empty_count == 4:
            continue
        elif l.count(turn) == 4:
            score += 1000000000
        elif l.count(opp[turn]) == 4:
            score -= 1000000000
        elif empty_count == 4 - l.count(turn):
            score += (4 - empty_count)
            if empty_count == 1:
                multiple_threats += 1
        elif empty_count == 4 - l.count(opp[turn]):
            score -= (4 - empty_count)
            if empty_count == 1:
                multiple_blocks += 1
        # elif l.count(turn) == 3 and empty_count == 1:
        #     score += 3
        #     multiple_threats += 1
        # elif l.count(opp[turn]) == 3 and empty_count == 1:
        #     score -= 3
        #     multiple_blocks += 1
        # elif l.count(turn) == 2 and empty_count == 2:
        #     score += 2
        # elif l.count(opp[turn]) == 2 and empty_count == 2:
        #     score -= 2
        # elif l.count(turn) == 1 and empty_count == 3:
        #     score += 1
        # elif l.count(opp[turn]) == 1 and empty_count == 3:
        #     score -= 1

    if multiple_threats > 1:
        score += 5 * multiple_threats
    if multiple_blocks > 1:
        score -= 5 * multiple_blocks

    return score

def possible_moves(board, turn, win_table):
    moves = [col for col in range(len(board[0])) if board[0][col] == '.']
    moves_scores = []
    for move in moves:
        temp_board = make_move(move, turn, board)
        score = heuristic(temp_board, turn, win_table, 0)
        moves_scores.append((move, score))
    moves_scores.sort(key=lambda x: x[1], reverse=True)
    return [move for move, score in moves_scores]

def make_move(col, turn, board):
    new_board = [['.' for _ in range(7)] for _ in range(6)]
    for r in range(len(board)):
        for c in range(len(board[0])):
            new_board[r][c] = board[r][c]
    row = -1
    for r in range(5, -1, -1):
        if new_board[r][col] == '.':
            row = r
            break
    if row == -1:
        raise ValueError
    new_board[row][col] = turn
    return new_board

def end_test(board, win_table):
    for i in win_table:
        if board[i[0][0]][i[0][1]] == board[i[1][0]][i[1][1]] == \
           board[i[2][0]][i[2][1]] == board[i[3][0]][i[3][1]] and board[i[0][0]][i[0][1]] != '.':
            return (True, board[i[0][0]][i[0][1]])
    count = 0
    for r in board:
        count += r.count('.')
    if count == 0:
        return (True, '')
    return (False, '')

def display(board):
    output = ''
    for r in range(6):
        output += ' '.join(board[r]) + '\n'
    return output

def main():
    ai = input("Which color is the AI (R or Y)? ").upper()

    board = [['.' for _ in range(7)] for _ in range(6)]
    print(display(board))

    win_table = create_win_table()
    turn = 'R'
    depth = 9

    while end_test(board, win_table)[0] == False:
        if turn != ai:
            col = int(input(f"It's {turn}'s turn. Choose a column: "))
            if col < 1 or col > 7:
                print("That is not a valid column.")
                continue
            
            try:
                new_board = make_move(col - 1, turn, board)
            except:
                print("That column is full.")
                continue
        else:
            t = time.time()
            move = minimax(board, turn, ai, win_table, depth, -9999, 9999, True)[0]
            new_board = make_move(move, turn, board)
            print(time.time() - t)
        
        board = new_board
        print(display(board))

        turn = opp[turn]

    winner = end_test(board, win_table)[1]
    if winner == '':
        print("Game over! It's a tie.")
    else:
        print(f"Game over! {winner} won.")

if __name__ == '__main__':
    main()