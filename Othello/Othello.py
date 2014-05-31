import copy
import pygame
import sys
from pygame.locals import *

pygame.init()

# Constant values used throughout the code
white = 1
black = -1
empty = 0
size = 10
maxDepth = 10

cell_width = 70
cell_height = 70
grid_width = 5
grid_padding = 10

board_width = 615
board_height = 615

pass_button = pygame.Rect((450, 625, 95, 43))

basicFont = pygame.font.SysFont(None, 48)
tahoma = pygame.font.SysFont('tahoma', 36)
helvetica = pygame.font.SysFont('helvetica', 28)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class OthelloBoard:
    '''An Othello board, with a variety of methods for managing a game.'''
    
    def __init__(self,array):
        '''If the parameter 'board' is left out, then the game board
        is initialized to its typical starting postion. Alternatively,
        a two-dimensional list with a pre-existing starting position
        can be supplied as well. Note that the size of the board is
        10x10, instead of 8x8; this is because leaving a blank ring
        around the edge of the board makes the rest of the code much
        simpler.'''
        if len(array) == 0:
            self.array = [[empty]*size for i in range(size)]
            self.array[4][4] = white
            self.array[5][5] = white
            self.array[4][5] = black
            self.array[5][4] = black
        else:
            self.array = array[:]

    def display(self, player_name):
        '''Displays the current board to the terminal window, with
        headers across the left and top. While some might accuse this
        text output as being "old school," having a scrollable game
        history actually makes debugging much easier.'''
#        screen = pygame.display.set_mode((640,640))
        windowSurface = pygame.display.set_mode((board_width, board_height+75), 0, 32)
        windowSurface.fill(pygame.Color(25,25,25)) #setting the background color
        statusbar = pygame.Rect(10, 615, 595, 65)
        pygame.draw.rect(windowSurface, (34, 158, 0), statusbar)
                
        text = helvetica.render(player_name + '\'s turn', True, WHITE)
        windowSurface.blit(text, (30, 625))
        
        stroke = 2
        
        pygame.draw.rect(windowSurface, BLACK, pass_button, stroke)
        
        w = pass_button.width - 4
        h = pass_button.height - 4
        x = pass_button.x + 2
        y = pass_button.y + 2
        pass_button_inner = pygame.Rect((x,y,w,h))

        pygame.draw.rect(windowSurface, (24, 128, 0), pass_button_inner)
        
        pass_text = tahoma.render('Pass', True, WHITE)
        windowSurface.blit(pass_text, (pass_button.x+10, pass_button.y-3))
        pygame.display.update()
        
        print ' ',
        for i in range(1,9):
            print i,
        print 
        
        for k in range(8): 
            for j in range(8):
                cell = pygame.Rect((k*cell_height) + grid_width*k + grid_padding, (j*cell_width) + grid_width*j + grid_padding, cell_width, cell_height)
                pygame.draw.rect(windowSurface, (31, 156, 191), cell)
    
        for i in range(0,9): 
            for j in range(0,9):
                center = (( j*(cell_height+grid_width) + ((cell_height)/2) + grid_padding), ( i*(cell_height+grid_width) + ((cell_height)/2) + grid_padding))
                radius = (cell_width/2 - 5)
                if self.array[i+1][j+1] == white:
                    pygame.draw.circle(windowSurface, (255, 255, 255), center, radius, 0)
                elif self.array[i+1][j+1] == black:
                    pygame.draw.circle(windowSurface, (0,0,0), center, radius, 0)
        
        pygame.display.update()
        
        for i in range(1,9):
            print i, 
            for j in range(1,9):
                if self.array[i][j] == white:
                    print 'W',
                elif self.array[i][j] == black:
                    print 'B',
                else:
                    print '-',
            print
        pygame.display.update() 

    def makeMove(self,row,col,piece):
        ''' Returns None if move is not legal. Otherwise returns an
        updated OthelloBoard, which is a copy of the original.'''

        # A move cannot be made if a piece is already there.
        if self.array[row][col] != empty:
             return None

        # A move cannot be made if the piece "value" is not black or white.
        if piece != black and piece != white:
            return None

        # Make a copy of the board (not just the pointer!)
        bcopy = copy.deepcopy(self.array)
        bcopy[row][col] = piece

        # Ranges for use below
        rowup = range(row+1,size)
        rowdown = range(row-1,-1,-1)
        rowfixed = [row for i in range(size)]
        colup = range(col+1,size)
        coldown = range(col-1,-1,-1)
        colfixed = [col for i in range(size)]

        # Set up ranges of tuples representing all eight directions.
        vectors = [zip(rowup,coldown),zip(rowup,colfixed), \
                zip(rowup,colup), zip(rowdown,coldown), \
                zip(rowdown, colfixed), zip(rowdown,colup), \
                zip(rowfixed,coldown), zip(rowfixed,colup)]

        # Try to make a move in each direction. Record if at least one
        # of them succeeds.
        flipped = False
        for vector in vectors:

            # Determine how far you can go in this direction. If you
            # see the opponent's piece, that's a candidate for
            # flipping: count and keep moving. If you see your own
            # piece, that's the end of the range and you're done. If
            # you see a blank space, you must not have had one of your
            # own pieces on the other end of the range.
            count = 0
            for (r,c) in vector:
                if bcopy[r][c] == -1*piece:
                    count += 1
                elif bcopy[r][c] == piece:
                    break
                else:
                    count = 0
                    break

            # If range is nontrivial, then it's a successful move.
            if count > 0:
                flipped = True

            # Actually record the flips.
            for i in range(count):
                (r,c) = vector[i]
                bcopy[r][c] = piece

        if flipped:
            return OthelloBoard(bcopy)
        else:
            return None
    
                         
    def _legalMoves(self,color):
        '''To be a legal move, the space must be blank, and you must take at
        least one piece. Note that this method works by attempting to
        move at each possible square, and recording which moves
        succeed. Therefore, using this method in order to try to limit
        which spaces you actually use in makeMoves is futile.'''
        moves = []
        for i in range(1,size-1):
            for j in range(1,size-1):
                bcopy = self.makeMove(i,j,color)
                if bcopy != None:
                    moves.append((i,j))
        return moves

    def scores(self):
        '''Returns a list of black and white scores for the current board.'''
        score = [0,0]
        for i in range(1,size-1):
            for j in range(1,size-1):
                if self.array[i][j] == black:
                    score[0] += 1
                elif self.array[i][j] == white:
                    score[1] += 1
        return score


    def playGame(self):
        '''Manages playing an actual game of Othello.'''
        
        print 'Black goes first.'
        # Two player objects: [black, white]
        players = [None, None]
        colorNames = ('black', 'white')
        colorValues = (black, white)
        invalidPasses = [0, 0]
        illegalMoves = [0, 0]

        # Determine whether each player is human or computer, and
        # instantiate accordingly
        for i in range(2):
            response = raw_input('Should ' + colorNames[i] + \
                             ' be (h)uman or (c)omputer? ')
            if response.lower() == 'h':
                name = raw_input("What is the player's name? ")
                players[i] = HumanPlayer(name,colorValues[i])
            else:
                plies = int(raw_input("How many plies ahead " + \
                                  "should the computer look? "))
                players[i] = ComputerPlayer(
                               'compy' + colorNames[i],colorValues[i], self.heuristic,plies)

        # Number of times a "pass" move has been made, in a row
        passes = 0

        done = False
        curBoard = self
        while not done:
            # Black goes, then white
            for i in range(2):

                # Display board and statistics
                curBoard.display(players[i].name)
                scores = curBoard.scores()
                print 'Statistics: score / invalid passes / illegal moves'
                for j in range(2):
                    print colorNames[j] + ':',scores[j], '/', \
                          invalidPasses[j], '/',illegalMoves[j]
                print
                print 'Turn:',colorNames[i]

                # Obtain move that player makes
                move = players[i].chooseMove(curBoard)

                if move == None:
                    # If no move is made, that is considered a
                    # pass. Verify that there were in fact no legal
                    # moves available. If there were, allow the pass
                    # anyway (this is easier to code), but record that
                    # an invalid pass was taken.

                    passes += 1
                    print colorNames[i] + ' passes.'
                    legalMoves=curBoard._legalMoves(colorValues[i])
                    if legalMoves != []:
                        print colorNames[i] + \
                              ' passed, but there was a legal move.'
                        print 'Legal moves: ' + str(legalMoves)
                        invalidPasses[i] += 1
                else:
                    # If a move is made, make the move on the
                    # board. makeMove returns None if the move is
                    # illegal. Record as an illegal move, and forfeit
                    # the player's turn. This is easier to code than
                    # offering another turn.

                    passes = 0
                    print colorNames[i] + ' chooses ' + str(move) + '.'
                    bcopy = curBoard.makeMove(move[0],move[1],colorValues[i])
                    while bcopy == None:
                        print 'That move is illegal, please choose another move.'
                        move = players[i].chooseMove(curBoard)
                        print colorNames[i] + ' chooses ' + str(move) + '.'
                        bcopy = curBoard.makeMove(move[0],move[1],colorValues[i]) 
                    
                    curBoard = bcopy
                print

                # To keep code simple, never test for win or loss; if
                # one player has won, lost, or tied, two passes must
                # occur in a row.
                if passes == 2:
                    print 'Both players passed, game is over.'
                    done = True
                    break

        # Display final outcome
        scores = curBoard.scores()
        if scores[0] > scores[1]:
            print 'Black wins!'
        elif scores[1] > scores[0]:
            print 'White wins!'
        else:
            print 'Tie game!'
            
    def heuristic(self):
        '''This very silly heuristic just adds up all the 1s, -1s, and 0s stored on the othello board.'''
        scoreSum = 0
        for i in range(1,size-1): #rows 
            for j in range(1,size-1):#columns 
                if (((i==1) or (i ==size-1)) and ((j==1) or (j==size-1))):  #all corners are worth 5 times the points 
                    scoreSum += 5*(self.array[i][j])
                elif (((i >=3) and (i<=6)) and ((j==3) or (j==6))) or (((i==4) or (i==5)) and ((j==4) or (j==5))):
                    scoreSum+= 4*(self.array[i][j])
                elif (((i>=3) and (i<=6)) and ((j==1) or (j==size-1))) or (((i==1) or (i==size-1)) and ((j>=3) and (j<=6))): 
                    scoreSum += 3*(self.array[i][j])
                elif (((i>=3) and (i<=6)) and ((j==2) or (j==size-2))) or (((i==2) or (i==size-2)) and ((j>=3) and (j<=6))): 
                    scoreSum += 2*(self.array[i][j])
                elif (((i==1) or (i==size-1)) and ((j==2) or (j==size-2))) or (((i==2) or (i==size-2)) and ((j<=2) or (j>=size-2))):
                    scoreSum += self.array[i][j]
        return scoreSum
            
class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
    
    def check_grid_click(self, mouseX, mouseY):
        if mouseX < grid_padding or mouseX > (grid_padding + 8*(cell_width + grid_width)):
            return True
        if mouseY < grid_padding or mouseY > (grid_padding + 8*(cell_height + grid_width)):
            return True
        for i in range(1, 7):
            for j in range(5):
                if mouseX == (grid_padding + i*(cell_width + grid_width)) - j:
                    return True
                elif mouseY == (grid_padding + i*(cell_height + grid_width)) - j:
                    return True
        return False
        
    def chooseMove(self,board):
        turnEnd = False
        while not turnEnd:
#            try:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    
                    if mouseX >= pass_button.x-2 and mouseX <= pass_button.x + pass_button.width+2 and \
                        mouseY >= pass_button.y-2 and mouseY <= pass_button.y + pass_button.height+2:
                            # Return no moves if the pass button is clicked
                            return None
                    
                    if self.check_grid_click(mouseX, mouseY):
                        print 'You did not click on a tile. Please re-select your move.'
                        # Get to the while statement
                        break;
                    
                    boxX = (mouseX - grid_padding)/(cell_width + grid_width)
                    boxY = (mouseY - grid_padding)/(cell_height + grid_width)
                    
                    move = (boxY + 1, boxX + 1)
                    
                    if len(move)==2 and type(move[0])==int and \
                        type(move[1])==int and (move[0] in range(1,9) and \
                        move[1] in range(1,9) or move == (0,0)):
                            turnEnd = True
                    else:
                        print 'Illegal entry, try again. (First one)'
                        
#            except Exception:
#                print 'Illegal entry, try again.'

        if move == (0,0):
            return None
        else:
            return move
        
#    def chooseMove(self,board):
#        while True:
#            try:
#                move = eval('(' + raw_input(self.name + \
#                ': enter row, column (or type "0,0" if no legal move): ') \
#                + ')')
#                if len(move)==2 and type(move[0])==int and \
#                type(move[1])==int and (move[0] in range(1,9) and \
#                move[1] in range(1,9) or move == (0,0)):
#                    break
#                print 'Illegal entry, try again.'
#            except Exception:
#                print 'Illegal entry, try again.'
#            
#        if move == (0,0):
#            return None
#        else:
#            return move

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies):
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies

        if self.color == black:
            self.opponentColor = white
        else:
            self.opponentColor = black

    def chooseMove(self,board):
        '''Chooses a move based on the best move that the minimax function returns'''
        bestMove = self.minimax(board, self.plies, True, 1000, 1000)[0] # Minimax return values: (bestMove, alpha/beta)
        
        return bestMove
        
    def minimax(self, node, depth, maximizing, alpha, beta):
        '''Recursively looks a certain number of plies ahead to determine the best move'''
        if depth == 0 or not node._legalMoves(self.color): # Base case - returns Roxanne heuristic of the board
            return None, self.color * node.heuristic()
        else:
            bestMove = None
            
            if maximizing: # Is it the computer's turn?
                node_legalMoves = node._legalMoves(self.color)
            else:          # Or the opponent's turn?
                node_legalMoves = node._legalMoves(self.opponentColor)
                
            for i in node_legalMoves:
                if maximizing:
                    branch = node.makeMove(i[0], i[1], self.color)
                else:
                    branch = node.makeMove(i[0], i[1], self.opponentColor)
                    
                nextMove, val = self.minimax(branch, depth-1, not maximizing, alpha, beta)
                val = -val # <---------------------- The tree will look like this:
                                                    #              3
                if val < alpha and maximizing:      #             / \
                    alpha = val                     #           -3  -1 <---- Picks the largest branch
                    bestMove = i                    #           /\  /\       and negates it
                if val < beta and not maximizing:   #          3 1 1 -2
                    beta = val
                    bestMove = i
                if alpha != 1000 and beta != -1000 and alpha <= -beta: # Ignores branches that don't need to be checked
                    break                                              # Sometimes, it's mathematically impossible for certain branches 
            if maximizing:                                             #      to be better than other branches, so they become pruned
                return bestMove, alpha
            return bestMove, beta
            
if __name__=='__main__':
    OthelloBoard([]).playGame()
    
    while True:
        playing = True 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()        