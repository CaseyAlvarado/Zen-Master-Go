class TicTacToe:
    """ Encodes the state of the Tic Tac Toe board """
    def __init__(self, player_mark, computer_mark):
        self.player_mark = player_mark
        self.computer_mark = computer_mark
        self.board = ['-', '-', '-',
                      '-', '-', '-',
                      '-', '-', '-']
        
    def check_victory(self, board): 
        a_play = board[0] == board[3] == board[6] == self.player_mark  #Various conditions
        b_play = board[1] == board[4] == board[7] == self.player_mark  #for winning the game
        c_play = board[2] == board[5] == board[8] == self.player_mark
        d_play = board[0] == board[1] == board[2] == self.player_mark
        e_play = board[3] == board[4] == board[5] == self.player_mark
        f_play = board[6] == board[7] == board[8] == self.player_mark
        g_play = board[0] == board[4] == board[8] == self.player_mark
        h_play = board[2] == board[4] == board[6] == self.player_mark
        
        a_comp = board[0] == board[3] == board[6] == self.computer_mark  #Various conditions
        b_comp = board[1] == board[4] == board[7] == self.computer_mark #for winning the game
        c_comp = board[2] == board[5] == board[8] == self.computer_mark
        d_comp = board[0] == board[1] == board[2] == self.computer_mark
        e_comp = board[3] == board[4] == board[5] == self.computer_mark
        f_comp = board[6] == board[7] == board[8] == self.computer_mark
        g_comp = board[0] == board[4] == board[8] == self.computer_mark
        h_comp = board[2] == board[4] == board[6] == self.computer_mark
        
        if a_play or b_play or c_play or d_play or e_play or f_play or g_play or h_play: #Checks if any of these conditions are satisfied
            return (True, "The player") #Returns if a victory has been found and the winner
        elif a_comp or b_comp or c_comp or d_comp or e_comp or f_comp or g_comp or h_comp:
            return (True, "The computer")
        else:
            return (False, None)
            
    def check_stalemate(self, board):
        for i in board:
            if i == '-':
                return False
        return True
    
    def evaluate_board(self):
        victor = self.check_victory(self.board)
        if victor[0]:
            if victor[1] == "The player":
                return -1
            return 1
        return 0
            
    def player_move(self):
        mark = int(raw_input("What's your next move? ")) # Index from 0 to 8
        while(self.board[mark] != '-'):
            print "Invalid move."
            mark = int(raw_input("What's your next move? ")) # Index from 0 to 8
            
        self.board[mark] = self.player_mark
    
    def computer_move(self):
        next_move = self.minimax(self.board, 10, True, 9)
        self.board[next_move[1]] = self.computer_mark
        
    def find_blanks(self, board):
        blanks = []
        
        for i in range(len(board)):
            if board[i] == '-':
                blanks.append(i)
        
        return blanks
    
    def minimax(self, board, depth, comp_turn, comp_move):
        if depth == 0 or self.check_victory(self.board)[0]:
            return (self.evaluate_board(), comp_move)
        
        if self.check_stalemate(self.board):
            return (0, comp_move)
            
        possible_moves = self.find_blanks(self.board)
        
        if comp_turn == True:
            best_value = -1000
            comp_move = possible_moves[0]
            for move in possible_moves:
                self.board[move] = self.computer_mark
                value = self.minimax(self.board, depth-1, False, comp_move)[0]
                self.board[move] = '-'
                if value > best_value:
                    best_value = value
                    comp_move = move
            return (best_value, comp_move)
        
        if comp_turn == False:
            best_value = 1000
            comp_move = possible_moves[0]
            for move in possible_moves:
                self.board[move] = self.player_mark
                value = self.minimax(self.board, depth-1, True, comp_move)[0]
                self.board[move] = '-'
                if value < best_value:
                    best_value = value
                    comp_move = move
            return (best_value, comp_move)
        
    def display_board(self):
        for i in range(3):
            print str(self.board[i*3]) + " " + str(self.board[i*3+1]) + " " + str(self.board[i*3+2])
        
if __name__ == '__main__':    
    first_player = raw_input("Who will go first? ") # You or me?
        
    if first_player == "me":
        game = TicTacToe('X', 'O')
    elif first_player == "you":
        game = TicTacToe('O', 'X')
        game.computer_move()
        
    game.display_board()

    while True:
        game.player_move()
        game.display_board()
        victory = game.check_victory(game.board)
        if victory[0] == True:
            print victory[1] + " wins!"
            break
        if game.check_stalemate(game.board):
            print "Stalemate!"
            break

        game.computer_move()
        game.display_board()
        victory = game.check_victory(game.board)
        if victory[0] == True:
            print victory[1] + " wins!"
            break
        if game.check_stalemate(game.board):
            print "Stalemate!"
            break
