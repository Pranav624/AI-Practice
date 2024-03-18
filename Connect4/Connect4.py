import time, pygame

opp = {'R': 'Y', 'Y': 'R'}
TABLE = {}
TABLE2 = {}
ENDTABLE = {}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)
WIDTH = 700
HEIGHT = 700

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

def minimax(board, turn, turn_num, ai, win_table, depth, alpha, beta, maximizing_player):
    if turn_num <= 2:
        return (3, 0)
    
    board_str = display(board)
    if (board_str, turn) in TABLE2:
        saved_depth, saved_value = TABLE2[(board_str, turn)]
        if saved_depth >= depth:
            return (0, saved_value)

    if depth == 0 or end_test(board, win_table)[0]:
        return (0, heuristic(board, ai, win_table, depth))
    moves = possible_moves(board, turn, win_table)
    if maximizing_player:
        value = -9999
        best_move = 0
        for move in moves:
            new_board = make_move(move, turn, board)
            new_value = minimax(new_board, opp[turn], turn_num+1, ai, win_table, depth - 1, alpha, beta, False)[1]
            if new_value > value:
                value = new_value
                best_move = move
            if value > beta:
                break
            alpha = max(alpha, value)
        TABLE2[(board_str, turn)] = (depth, value)
        return (best_move, value)
    else:
        value = 9999
        best_move = 0
        for move in moves:
            new_board = make_move(move, turn, board)
            new_value = minimax(new_board, opp[turn], turn_num+1, ai, win_table, depth - 1, alpha, beta, True)[1]
            if new_value < value:
                value = new_value
                best_move = move
            if value < alpha:
                break
            beta = min(beta, value)
        TABLE2[(board_str, turn)] = (depth, value)
        return (best_move, value)

def heuristic(board, turn, win_table, depth):
    board_str = display(board)
    if (board_str, turn) in TABLE:
        return TABLE[(board_str, turn)]
    
    score = 0
    multiple_threats = 0
    multiple_blocks = 0

    for i in win_table:
        l = [board[i[j][0]][i[j][1]] for j in range(4)]

        empty_count = l.count('.')
        if empty_count == 4:
            continue
        elif empty_count == 4 - l.count(turn):
            score += (4 - empty_count)
            if empty_count == 1:
                multiple_threats += 1
            elif empty_count == 0:
                score += 1000
        elif empty_count == 4 - l.count(opp[turn]):
            score -= (4 - empty_count)
            if empty_count == 1:
                multiple_blocks += 1
            elif empty_count == 0:
                score -= 1000

    if multiple_threats > 1:
        score += 5 * multiple_threats
    if multiple_blocks > 1:
        score -= 5 * multiple_blocks

    TABLE[(board_str, turn)] = score
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
    new_board = [row[:] for row in board]
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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption("Connect 4")
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Is the bot R or Y?", True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT - 50)
    
    board = [['.' for _ in range(7)] for _ in range(6)]

    pygame.draw.rect(screen, BLUE, [40, 40, 620, 560])
    for i in range(len(board)):
        for j in range(len(board[0])):
            pygame.draw.circle(screen, GRAY, (j*80+110, i*80+110), 30)
    screen.blit(text, textRect)
    pygame.display.update()

    # ai = input("Which color is the AI (R or Y)? ").upper()
    ai = ''
    while ai == '':
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    ai = 'R'
                    text = font.render(f"The bot is red!", True, BLACK, WHITE)
                    textRect = text.get_rect()
                    textRect.center = (WIDTH // 2, HEIGHT - 50)
                    screen.blit(text, textRect)
                    pygame.display.update()
                elif event.key == pygame.K_y:
                    ai = 'Y'
                    text = font.render(f"The bot is yellow, it's your turn!", True, BLACK, WHITE)
                    textRect = text.get_rect()
                    textRect.center = (WIDTH // 2, HEIGHT - 50)
                    screen.blit(text, textRect)
                    pygame.display.update()
    
    print(display(board))

    win_table = create_win_table()
    turn = 'R'
    turn_num = 1
    depth = 10

    while end_test(board, win_table)[0] == False:        
        if turn != ai:
            move_made = False
            col = -1
            while not move_made:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 70 <= pygame.mouse.get_pos()[0] <= 150:
                            col = 0
                            move_made = True
                        elif 150 <= pygame.mouse.get_pos()[0] <= 230:
                            col = 1
                            move_made = True
                        elif 230 <= pygame.mouse.get_pos()[0] <= 310:
                            col = 2
                            move_made = True
                        elif 310 <= pygame.mouse.get_pos()[0] <= 390:
                            col = 3
                            move_made = True
                        elif 390 <= pygame.mouse.get_pos()[0] <= 470:
                            col = 4
                            move_made = True
                        elif 470 <= pygame.mouse.get_pos()[0] <= 550:
                            col = 5
                            move_made = True
                        elif 550 <= pygame.mouse.get_pos()[0] <= 630:
                            col = 6
                            move_made = True        
            try:
                new_board = make_move(col, turn, board)
            except:
                # print("That column is full.")
                text = font.render('That column is full.', True, BLACK, WHITE)
                textRect = text.get_rect()
                textRect.center = (WIDTH // 2, HEIGHT - 50)
                screen.blit(text, textRect)
                continue
        else:
            print()
            t = time.time()
            move = minimax(board, turn, turn_num, ai, win_table, depth, -9999, 9999, True)[0]
            new_board = make_move(move, turn, board)
            text = font.render(f"Bot ({ai}) played {move + 1} in {round(time.time() - t, 2)} seconds.", True, BLACK, WHITE)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT - 50)
            screen.blit(text, textRect)
        
        board = new_board
        print(display(board))
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == '.':
                    pygame.draw.circle(screen, GRAY, (j*80+110, i*80+110), 30)
                elif board[i][j] == 'R':
                    pygame.draw.circle(screen, RED, (j*80+110, i*80+110), 30)
                else:
                    pygame.draw.circle(screen, YELLOW, (j*80+110, i*80+110), 30)
        pygame.display.update()

        turn = opp[turn]
        turn_num += 1

    winner = end_test(board, win_table)[1]
    if winner == '':
        text = font.render("Game over! It's a tie.", True, BLACK, WHITE)
    else:
        text = font.render(f"Game over! {winner} won.", True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, 50)
    screen.blit(text, textRect)
    pygame.display.update()
    time.sleep(10)

if __name__ == '__main__':
    main()