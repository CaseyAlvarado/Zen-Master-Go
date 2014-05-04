import copy

import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.font.init() 
# Constant values used throughout the code
white = 1
black = -1
empty = 0
size = 8
length_of_board = 10
side_length = 640
rows = 8
columns = 8
#size = 10
#maxDepth = 10
cell_width = 80
cell_height = 80

class OthelloBoard:
    '''An Othello board, with a variety of methods for managing a game.'''
    
    def __init__(self, array):
        '''If the parameter 'board' is left out, then the game board
is initialized to its typical starting postion. Alternatively,
a two-dimensional list with a pre-existing starting position
can be supplied as well. Note that the size of the board is
10x10, instead of 8x8; this is because leaving a blank ring
around the edge of the board makes the rest of the code much
simpler.'''
        global length_of_board
        self.length_of_board = length_of_board
# self.curBoard = curBoard
        if len(array) == 0:
            self.array = [[empty]*length_of_board for i in range(self.length_of_board)]
            self.array[4][4] = white
            self.array[5][5] = white
            self.array[4][5] = black
            self.array[5][4] = black
        else:
            self.array = array[:]

    def display(self):
        '''Displays the current board to the terminal window, with
headers across the left and top. While some might accuse this
text output as being "old school," having a scrollable game
history actually makes debugging much easier.'''
        print ' ',
        for i in range(1, rows+1):
            print i,
        print
        print
        for i in range(1,rows+1):
            print i, '',
            for j in range(1,columns +1):
                if self.array[i][j] == white:
                    print 'W',
                elif self.array[i][j] == black:
                    print 'B',
                else:
                    print '-',
            print

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
    
    def heuristic(self):
        '''This very silly heuristic just adds up all the 1s, -1s, and 0s stored on the othello board.'''
        scoreSum = 0
        for i in range(1,size-1): #rows
            for j in range(1,size-1):#columns
                if (((i==1) or (i ==size-1)) and ((j==1) or (j==size-1))): #all corners are worth 5 times the points
                    scoreSum+=5*(self.array[i][j])
                elif (((i >=3) and (i<=6)) and ((j==3) or (j==6))) or (((i==4) or (i==5)) and ((j==4) or (j==5))):
                    scoreSum+=4*(self.array[i][j])
                elif (((i>=3) and (i<=6)) and ((j==1) or (j==size-1))) or (((i==1) or (i==size-1)) and ((j>=3) and (j<=6))):
                    scoreSum+=3*(self.array[i][j])
                elif (((i>=3) and (i<=6)) and ((j==2) or (j==size-2))) or (((i==2) or (i==size-2)) and ((j>=3) and (j<=6))):
                    scoreSum += 2*(self.array[i][j])
                elif (((i==1) or (i==size-1)) and ((j==2) or (j==size-2))) or (((i==2) or (i==size-2)) and ((j<=2) or (j>=size-2))):
                    scoreSum+= self.array[i][j]
        return scoreSum

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self, name, color, heuristic, plies):
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies
        self.invalidPasses = 0
        self.illegalMoves = 0

        if self.color == black:
            self.opponentColor = white
        else:
            self.opponentColor = black

    def chooseMove(self, board):
        '''Chooses a move based on the best move that the minimax function returns'''
        bestMove = self.minimax(board, self.plies, True, 1000, 1000)[0] # Minimax return values: (bestMove, alpha/beta)
        print bestMove
        return bestMove
        
    def minimax(self, node, depth, maximizing, alpha, beta):
        '''Recursively looks a certain number of plies ahead to determine the best move'''
        if depth == 0 or not node._legalMoves(self.color): # Base case - returns Roxanne heuristic of the board
            return None, self.color * node.heuristic()
        else:
            bestMove = None
            
            if maximizing: # Is it the computer's turn?
                node_legalMoves = node._legalMoves(self.color)
            else: # Or the opponent's turn?
                node_legalMoves = node._legalMoves(self.opponentColor)
                
            for i in node_legalMoves:
                if maximizing:
                    branch = node.makeMove(i[0], i[1], self.color)
                else:
                    branch = node.makeMove(i[0], i[1], self.opponentColor)
                    
                nextMove, val = self.minimax(branch, depth-1, not maximizing, alpha, beta)
                val = -val # <---------------------- The tree will look like this:
                                                    # 3
                if val < alpha and maximizing: # / \
                    alpha = val # -3 -1 <---- Picks the largest branch
                    bestMove = i # /\ /\ and negates it
                if val < beta and not maximizing: # 3 1 1 -2
                    beta = val
                    bestMove = i
                if alpha != 1000 and beta != -1000 and alpha <= -beta: # Ignores branches that don't need to be checked
                    break # Sometimes, it's mathematically impossible for certain branches
            if maximizing: # to be better than other branches, so they become pruned
                return bestMove, alpha
            return bestMove, beta

class HumanPlayer:
    '''Human player: because it bothers Casey'''
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.invalidPasses = 0
        self.illegalMoves = 0
    
    def chooseMove(self, board):
        while True:
            try:
#                move = eval('(' + raw_input(self.name + \
#                 ': enter row, column (or type "0,0" if no legal move): ') \
#                 + ')')

                if len(move)==2 and type(move[0])==int and \
                   type(move[1])==int and (move[0] in range(1,9) and \
                   move[1] in range(1,9) or move==(0,0)):
                    break

                    print 'Illegal entry, try again.'
            except Exception:
                print 'Illegal entry, try again.'

        if move==(0,0):
            return None
        else:
            return move

class OthelloModel:
    def __init__(self, board):
        self.board = board
        self.colorValues = (black, white)
        self.colorNames = ('black', 'white')
        self.players = [None, None]
        self.scores = [0, 0]
        self.passes = 0
        
        self.make_players()
        
    def make_players(self):
        """ This also bothers you"""
        print 'Black goes first'
        
        for i in range(2):
            response = raw_input('Should ' + self.colorNames[i] + ' be (h)uman or (c)omputer? ')
            
            if response.lower() == 'h':
                name = raw_input("What is the player's name? ")
                self.players[i] = HumanPlayer(name, self.colorValues[i])
            else:
                plies = int(raw_input("How many plies ahead should the computer look? "))
                start_heuristic = 0
                self.players[i] = ComputerPlayer('compy' + self.colorNames[i], self.colorValues[i], start_heuristic, plies)
        
    def playGame(self):
        '''Manages playing an actual game of Othello.'''
        # Two player objects: [black, white]
        colorNames = ('black', 'white')
        
        # Number of times a "pass" move has been made, in a row
# passes = 0
# done = False
        
        self.board.display()
        
        
        print
        for i in range(2):
            # Display board and statistics
# curBoard.display()
# view.drawBoard(curBoard)
            self.scores = self.board.scores()
            print 'Statistics: score / invalid passes / illegal moves'
            for j in range(2):
                print colorNames[j] + ':',self.board.scores()[j], '/', \
                      self.players[j].invalidPasses, '/', self.players[j].illegalMoves
            print
            print 'Turn:', colorNames[i]

            # Obtain move that player makes
            move = self.players[i].chooseMove(self.board)

            if move == None:
                # If no move is made, that is considered a
                # pass. Verify that there were in fact no legal
                # moves available. If there were, allow the pass
                # anyway (this is easier to code), but record that
                # an invalid pass was taken.
                
                self.passes += 1
                print colorNames[i] + ' passes.'
                legalMoves=self.board._legalMoves(self.colorValues[i])
                if legalMoves != []:
                    print colorNames[i] + \
                          ' passed, but there was a legal move.'
                    print 'Legal moves: ' + str(legalMoves)
                    self.players[i].invalidPasses += 1
            else:
                # If a move is made, make the move on the
                # board. makeMove returns None if the move is
                # illegal. Record as an illegal move, and forfeit
                # the player's turn. This is easier to code than
                # offering another turn.

                self.passes = 0
                print colorNames[i] + ' chooses ' + str(move) + '.'
                bcopy = self.board.makeMove(move[0],move[1],self.colorValues[i])
                if bcopy == None:
                    print 'That move is illegal, turn is forfeited.'
                    self.players[i].illegalMoves += 1
                else:
                    self.board = bcopy

            # To keep code simple, never test for win or loss; if
            # one player has won, lost, or tied, two passes must
            # occur in a row.
            
class ViewingPurposes:
    def __init__(self, model, screen, array):
        self.model = model
        self.screen = screen
        
    
    def drawBoard(self):
        print "before screen fill"
        self.screen.fill(pygame.Color(255,255,255)) #setting background color
        print "after screen fill"
        rows = 8
        columns = 8
        for i in range(len(self.model.array[0])):
            for j in range(len(self.model.array[1])):
                cell = pygame.Rect((i*self.cell_height), (j*self.cell_width), self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, (200, 5, 156), cell)
                
        #draw the four original circles
        #pygame.draw.circle(Surface, color, position, radius, width)
        
        ##then while loop with updating circles
        for k in range(len(self.model.array[0])): 
            for c in range(len(self.model.array[1])):  
                center = ((k*cell_height + ((k*cell_height)/2.0)), (c*cell_height +((c*cell_height)/2.0)))
                if self.model.array[k][c] == white:
                    pygame.draw.circle(self.screen, center,(255,255,255))
                elif self.model.array[k][c] == black: 
                    pygame.draw.circle(self.screen, center, (0,0,0))
        
        
        center1 = ((4*cell_height + ((4*cell_height)/2.0)), (4*cell_height +((4*cell_height)/2.0)))
        pygame.draw.circle(self.screen, center1, white)
        center2 = ((5*cell_height + ((5*cell_height)/2.0)), (5*cell_height +((5*cell_height)/2.0)))
        pygame.draw.circle(self.screen, center2, white)
        center3 = ((4*cell_height + ((4*cell_height)/2.0)), (5*cell_height +((5*cell_height)/2.0)))
        pygame.draw.circle(self.screen, center3, black)
        center4 = ((5*cell_height + ((5*cell_height)/2.0)), (4*cell_height +((4*cell_height)/2.0)))
        pygame.draw.circle(self.screen, center4, black)
        
    def updateBoard(self): 
        for k in range(len(self.array[0])):
            for c in range(len(self.array[1])):
                center = ((k*cell_height + ((k*cell_height)/2.0)), (c*cell_height +((c*cell_height)/2.0)))
                if self.array[k][c] == white:
                    pygame.draw.circle(self.screen, center, (255,255,255), 0)
                elif self.array[k][c] == black:
                    pygame.draw.circle(self.screen,center,(0,0,0), 0)
                    
    def update(self):
         for i in range(1,size-1):
             
            for j in range(1,size-1):
                if self.array[i][j] == white:
                    print 'W',
                elif self.array[i][j] == black:
                    print 'B',
                else:
                    pass #what do I put here? CHECK THIS LATER
#    def question(self, message): 
##        windowSurface = pygame.display.set_mode((500, 400), 0, 32)
##        font = pygame.font.SysFont(None, 48)
##        text=font.render("BEEPP", True, (100,200,200))
##        textRect = text.get_rect()
##        textRect.centerx = windowSurface.get_rect().centerx
##        textRect.centery = windowSurface.get_rect().centery
##        windowSurface.blit(text, textRect)
##        pygame.display.update()
##        pygame.key.set_repeat(500, 30)
#        fontobject = pygame.font.Font(None,18)
#        if len(message) != 0:
#            windowSurface = pygame.display.set_mode((500, 400), 0, 32)
#            font = pygame.font.SysFont(None, 48)
#            text=font.render("BEEPP", True, (100,200,200))
#            textRect = text.get_rect()
#            textRect.centerx = windowSurface.get_rect().centerx
#            textRect.centery = windowSurface.get_rect().centery
#            windowSurface.blit(text, textRect)
#            pygame.display.update()
#            pygame.key.set_repeat(500, 30)
#            
##        pygame.display.flip()
#    def answering_quest(self, question): 
#            ##Answering the question 
#        pygame.font.init()
#        current_string = []
#        question(self.screen, question + ": " + string.join(current_string,""))
#        while 1:
#            inkey = get_key()
#            if inkey == K_BACKSPACE:
#                current_string = current_string[0:-1]
#            elif inkey == K_RETURN:
#                break
#            elif inkey == K_MINUS:
#                current_string.append("_")
#            elif inkey <= 127:
#                current_string.append(chr(inkey))
#            display_box(self.screen, question + ": " + string.join(current_string,""))
#            return string.join(current_string,"")
#        

class OthelloController:
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen 

    def which_box(self): 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            (mouseX, mouseY) = pygame.mouse.get_pos() 
            boxX = mouseX/cell_width
            boxY = mouseY/cell_height
        
        return (0+boxX, 0+boxY) 
        
        
if __name__=='__main__':
# '''Manages playing an actual game of Othello.'''
# screen = pygame.display.set_mode((self.length_of_board, self.length_of_board))
# view = ViewingPurposes(self, screen, self.array, cell_width, cell_height)

    sizetup = (640, 640)
    screen = pygame.display.set_mode(sizetup)

#
#    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
#    font = pygame.font.SysFont(None, 48)
#    text=font.render("BEEPP", True, (100,200,200))
#    textRect = text.get_rect()
#    textRect.centerx = windowSurface.get_rect().centerx
#    textRect.centery = windowSurface.get_rect().centery
#    windowSurface.blit(text, textRect)
#    pygame.display.update()
#    pygame.key.set_repeat(500, 30)

    model = OthelloModel(OthelloBoard([]))
    controller = OthelloController(model, screen)
    view = ViewingPurposes(model,screen)
    playing = True
    
    while True:
        view.drawBoard()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                if playing:
                    boxX = mouseX/cell_width
                    boxY = mouseY/cell_height
                    
                    # Two player objects: [black, white]
                    colorNames = ('black', 'white')
                    
                    # Number of times a "pass" move has been made, in a row                    
                    model.board.display()
                    
                    
                    print
                    for i in range(2):
                        # Display board and statistics
                        model.scores = model.board.scores()
                        print 'Statistics: score / invalid passes / illegal moves'
                        for j in range(2):
                            print colorNames[j] + ':',model.board.scores()[j], '/', \
                                  model.players[j].invalidPasses, '/', model.players[j].illegalMoves
                        print
                        print 'Turn:', colorNames[i]
            
                        # Obtain move that player makes
                        move = model.players[i].chooseMove(model.board)
            
                        if move == None:
                            # If no move is made, that is considered a
                            # pass. Verify that there were in fact no legal
                            # moves available. If there were, allow the pass
                            # anyway (this is easier to code), but record that
                            # an invalid pass was taken.
                            
                            model.passes += 1
                            print colorNames[i] + ' passes.'
                            legalMoves = model.board._legalMoves(model.colorValues[i])
                            if legalMoves != []:
                                print colorNames[i] + \
                                      ' passed, but there was a legal move.'
                                print 'Legal moves: ' + str(legalMoves)
                                model.players[i].invalidPasses += 1
                        else:
                            # If a move is made, make the move on the
                            # board. makeMove returns None if the move is
                            # illegal. Record as an illegal move, and forfeit
                            # the player's turn. This is easier to code than
                            # offering another turn.
            
                            model.passes = 0
                            print colorNames[i] + ' chooses ' + str(move) + '.'
                            bcopy = self.board.makeMove(move[0],move[1],model.colorValues[i])
                            if bcopy == None:
                                print 'That move is illegal, turn is forfeited.'
                                model.players[i].illegalMoves += 1
                            else:
                                model.board = bcopy
                    
                    # To keep code simple, never test for win or loss; if
                    # one player has won, lost, or tied, two passes must
                    # occur in a row.
                    
                    if model.passes == 2:
                        print 'Both players passed, game is over.'
                        playing = False
                        break
                    
                    view.updateBoard()