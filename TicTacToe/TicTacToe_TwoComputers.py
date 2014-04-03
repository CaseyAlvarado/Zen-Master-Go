import random, math

class TicTacToe:
    """ Encodes the state of the Tic Tac Toe board """
    def __init__(self, first_player):
        self.board = ['-', '-', '-',
                      '-', '-', '-',
                      '-', '-', '-']
        self.first_player = first_player
        
    def check_victory(self, comp1_mark, comp2_mark): 
        a_comp1 = self.board[0] == self.board[3] == self.board[6] == comp1_mark  #Various conditions
        b_comp1 = self.board[1] == self.board[4] == self.board[7] == comp1_mark #for winning the game
        c_comp1 = self.board[2] == self.board[5] == self.board[8] == comp1_mark
        d_comp1 = self.board[0] == self.board[1] == self.board[2] == comp1_mark
        e_comp1 = self.board[3] == self.board[4] == self.board[5] == comp1_mark
        f_comp1 = self.board[6] == self.board[7] == self.board[8] == comp1_mark
        g_comp1 = self.board[0] == self.board[4] == self.board[8] == comp1_mark
        h_comp1 = self.board[2] == self.board[4] == self.board[6] == comp1_mark
        
        a_comp2 = self.board[0] == self.board[3] == self.board[6] == comp2_mark  #Various conditions
        b_comp2 = self.board[1] == self.board[4] == self.board[7] == comp2_mark #for winning the game
        c_comp2 = self.board[2] == self.board[5] == self.board[8] == comp2_mark
        d_comp2 = self.board[0] == self.board[1] == self.board[2] == comp2_mark
        e_comp2 = self.board[3] == self.board[4] == self.board[5] == comp2_mark
        f_comp2 = self.board[6] == self.board[7] == self.board[8] == comp2_mark
        g_comp2 = self.board[0] == self.board[4] == self.board[8] == comp2_mark
        h_comp2 = self.board[2] == self.board[4] == self.board[6] == comp2_mark
        
        if a_comp1 or b_comp1 or c_comp1 or d_comp1 or e_comp1 or f_comp1 or g_comp1 or h_comp1: #Checks if any of these conditions are satisfied
            return (True, "Computer 1") #Returns if a victory has been found and the winner
        elif a_comp2 or b_comp2 or c_comp2 or d_comp2 or e_comp2 or f_comp2 or g_comp2 or h_comp2:
            return (True, "Computer 2")
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
    
    def computer1_move(self, symbol):
        possible_moves = []
        
        for i in range(len(self.board)):
            if self.board[i] == '-':
                possible_moves.append(i)
                
        print possible_moves
        random_move = random.randint(0,len(possible_moves)-1)
        self.board[possible_moves[random_move]] = symbol
        
        
    def computer2_move(self, symbol):
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
    print "Battle of the AIs"
    first_player = raw_input("Which computer will go first? ") #1 or 2
    game = TicTacToe(first_player)
    
    if first_player == "1":
        computer1_symbol = 'O'
        computer2_symbol = 'X'
    elif first_player == "2":
        computer1_symbol = 'X'
        computer2_symbol = 'O'
        game.computer2_move(computer2_symbol)
    
    game.display_board()
        
    while True:
        game.computer1_move(computer1_symbol)
        game.display_board()
        victory = game.check_victory(computer1_symbol, computer2_symbol)
        if victory[0] == True:
            print victory[1] + " wins!"
            break
        if game.check_stalemate():
            print "Stalemate!"
            break
        
        game.computer2_move(computer2_symbol)
        game.display_board()
        victory = game.check_victory(computer1_symbol, computer2_symbol)
        if victory[0] == True:
            print victory[1] + " wins!"
            break
        if game.check_stalemate():
            print "Stalemate!"
            break