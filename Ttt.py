class Tictactoe:
    def __init__(self):
        self.__table = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.__board = '.........'
        self.__player = ''
        self.__ai = ''
        self.opp = {'X': 'O', 'O': 'X'}

    def set_player(self, player):
        self.__player = player

    def set_ai(self, ai):
        self.__ai = ai

    def get_board(self):
        return self.__board
    
    def set_board(self, board):
        self.__board = board

    # Method for checking if game ended
    def end_test(self, board):
        if '.' not in board:
            return True
        for x in self.__table:
            temp = [board[i] for i in x]
            if len(set(temp)) == 1 and '.' not in set(temp):
                return True
        return False

    # Heuristic
    def heuristic(self, turn, board):
        for x in self.__table:
            temp = [board[i] for i in x]
            if len(set(temp)) == 1 and '.' not in set(temp):
                if temp[0] == turn:
                    return 1
                else:
                    return -1
        return 0

    # Minimax
    def minimax(self, board, turn, maximizing_player):
        moves = self.get_children(turn, board)
        if self.end_test(board):
            return (board, self.heuristic(self.__ai, board))
        if maximizing_player:
            value = -9999
            best_move = ''
            for move in moves:
                v = self.minimax(move, self.opp[turn], False)[1]
                if v > value:
                    value = v
                    best_move = move
            return (best_move, value)
        else:
            value = 9999
            best_move = ''
            for move in moves:
                v = self.minimax(move, self.opp[turn], True)[1]
                if v < value:
                    value = v
                    best_move = move
            return (best_move, value)

    # Get children
    def get_children(self, turn, board):
        return [board[:i] + turn + board[i+1:] for i in range(len(board)) if board[i] == '.']


    # Display
    def display(self):
        output = ''
        for i in range(9):
            output += self.__board[i] + '  '
            if i % 3 == 2:
                output += '\n\n'
        return output

    # Human play
    def make_move(self, turn, index):
        self.__board = self.__board[:index] + turn + self.__board[index+1:]

def main():
    t = Tictactoe()
    ai = input("Which Player is the AI (X or O)? ").upper()
    player = t.opp[ai]
    t.set_ai(ai)
    t.set_player(player)
    print(t.display())
    turn = 'X'
    while(t.end_test(t.get_board()) == False):
        if turn == player:
            move = int(input("What is your move? "))
            if t.get_board()[move] != '.':
                print("That is not a valid move.")
                continue
            t.make_move(turn, move)
        else:
            move = t.minimax(t.get_board(), turn, True)[0]
            t.set_board(move)
        print(t.display())
        turn = t.opp[turn]

    if t.heuristic(turn,t.get_board()) == 0:
        print("Game over! It's a tie.")
    else:
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        print(f"Game over! {turn} won.")
    

if __name__ == '__main__':
    main()