import random, math

class TicTacToe:
    """ Encodes the state of the Tic Tac Toe board """
    def __init__(self, first_player):
        self.first_player = first_player
        self.board = ['-', '-', '-',
                      '-', '-', '-',
                      '-', '-', '-']
        
    def check_victory(self, player_mark, computer_mark): 
        a_play = self.board[0] == self.board[3] == self.board[6] == player_mark  #Various conditions
        b_play = self.board[1] == self.board[4] == self.board[7] == player_mark #for winning the game
        c_play = self.board[2] == self.board[5] == self.board[8] == player_mark
        d_play = self.board[0] == self.board[1] == self.board[2] == player_mark
        e_play = self.board[3] == self.board[4] == self.board[5] == player_mark
        f_play = self.board[6] == self.board[7] == self.board[8] == player_mark
        g_play = self.board[0] == self.board[4] == self.board[8] == player_mark
        h_play = self.board[2] == self.board[4] == self.board[6] == player_mark
        
        a_comp = self.board[0] == self.board[3] == self.board[6] == computer_mark  #Various conditions
        b_comp = self.board[1] == self.board[4] == self.board[7] == computer_mark #for winning the game
        c_comp = self.board[2] == self.board[5] == self.board[8] == computer_mark
        d_comp = self.board[0] == self.board[1] == self.board[2] == computer_mark
        e_comp = self.board[3] == self.board[4] == self.board[5] == computer_mark
        f_comp = self.board[6] == self.board[7] == self.board[8] == computer_mark
        g_comp = self.board[0] == self.board[4] == self.board[8] == computer_mark
        h_comp = self.board[2] == self.board[4] == self.board[6] == computer_mark
        
        if a_play or b_play or c_play or d_play or e_play or f_play or g_play or h_play: #Checks if any of these conditions are satisfied
            return (True, "The player") #Returns if a victory has been found and the winner
        elif a_comp or b_comp or c_comp or d_comp or e_comp or f_comp or g_comp or h_comp:
            return (True, "The computer")
        else:
            return (False, None)
            
    def check_stalemate(self):
        for i in self.board:
            if i == '-':
                return False
        return True
            
    def player_move(self, symbol):
        mark = int(raw_input("What's your next move? ")) #Index from 0 to 8
        while(self.board[mark] != '-'):
            print "Invalid move."
            mark = int(raw_input("What's your next move? ")) #Index from 0 to 8    
            
        self.board[mark] = symbol
    
    def computer_move(self, symbol):
        possible_moves = []
        
        for i in range(len(self.board)):
            if self.board[i] == '-':
                possible_moves.append(i)
                
        print possible_moves
        random_move = random.randint(0,len(possible_moves)-1)
        self.board[possible_moves[random_move]] = symbol
        
    def display_board(self):
        for i in range(3):
            print str(self.board[i*3]) + " " + str(self.board[i*3+1]) + " " + str(self.board[i*3+2])
        
if __name__ == '__main__':
    first_player = raw_input("Who will go first? ") #You or me?
    game = TicTacToe(first_player)
    
    if first_player == "me":
        player_symbol = 'O'
        computer_symbol = 'X'
    elif first_player == "you":
        player_symbol = 'X'
        computer_symbol = 'O'
        game.computer_move(computer_symbol)
    
    game.display_board()
        
    while True:
        game.player_move(player_symbol)
        game.display_board()
        victory = game.check_victory(player_symbol, computer_symbol)
        if victory[0] == True:
            print victory[1] + " wins!"
            break
        if game.check_stalemate():
            print "Stalemate!"
            break
        
        game.computer_move(computer_symbol)
        game.display_board()
        victory = game.check_victory(player_symbol, computer_symbol)
        if victory[0] == True:
            print victory[1] + " wins!"
            break
        if game.check_stalemate():
            print "Stalemate!"
            break