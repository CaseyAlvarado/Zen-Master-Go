import copy

import pygame 
import pygame.locals 

# Constant values used throughout the code
white = 1
black = -1
empty = 0
size = 8
#size = 10
#maxDepth = 10

class OthelloBoard:
    '''An Othello board, with a variety of methods for managing a game.'''
    
    def __init__(self, array, length_of_board):
        '''If the parameter 'board' is left out, then the game board
        is initialized to its typical starting postion. Alternatively,
        a two-dimensional list with a pre-existing starting position
        can be supplied as well. Note that the size of the board is
        10x10, instead of 8x8; this is because leaving a blank ring
        around the edge of the board makes the rest of the code much
        simpler.'''
        self.length_of_board = length_of_board 
#        self.curBoard = curBoard
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
        print '  ',
        for i in range(1,9):
            print i,
        print
        print
        for i in range(1,size-1):
            print i, '',
            for j in range(1,size-1):
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


    def playPly(self, passes, done):
        '''Manages playing an actual game of Othello.'''
        # Black goes, then white
        for i in range(2):

            # Display board and statistics
#                curBoard.display()
#                view.drawBoard(curBoard)
            
            scores = self.curBoard.scores()
            print 'Statistics: score / invalid passes / illegal moves'
            for j in range(2):
                print colorNames[j] + ':',scores[j], '/', \
                      invalidPasses[j], '/',illegalMoves[j]
            print
            print 'Turn:',colorNames[i]

            # Obtain move that player makes
            move = players[i].chooseMove(self.curBoard)

            if move==None:
                # If no move is made, that is considered a
                # pass. Verify that there were in fact no legal
                # moves available. If there were, allow the pass
                # anyway (this is easier to code), but record that
                # an invalid pass was taken.

                passes += 1
                print colorNames[i] + ' passes.'
                legalMoves=self.curBoard._legalMoves(colorValues[i])
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
                bcopy = self.curBoard.makeMove(move[0],move[1],colorValues[i])
                if bcopy==None:
                    print 'That move is illegal, turn is forfeited.'
                    illegalMoves[i] += 1
                else:
                    self.curBoard = bcopy
            print

            # To keep code simple, never test for win or loss; if
            # one player has won, lost, or tied, two passes must
            # occur in a row.
            if passes == 2:
                print 'Both players passed, game is over.'
                done = True
                break
            
    
    def heuristic(self):
        '''This very silly heuristic just adds up all the 1s, -1s, and 0s stored on the othello board.'''
        scoreSum = 0
        for i in range(1,size-1): #rows 
            for j in range(1,size-1):#columns 
                if (((i==1) or (i ==size-1)) and ((j==1) or (j==size-1))):  #all corners are worth 5 times the points 
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
            
class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
        
    def chooseMove(self,board):
        while True:
            try:
                move = eval('(' + raw_input(self.name + \
                 ': enter row, column (or type "0,0" if no legal move): ') \
                 + ')')

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
        '''This very silly player just returns the first legal move
        that it finds.'''
        bestMove = self.minimax(board, self.plies, True)[0]
        
        if bestMove != (0,0):
            return bestMove
        return None
        
    def minimax(self, node, depth, maximizing):
        if depth == 0 or not node._legalMoves(self.color):
            return None, self.color * node.heuristic()
        else:
            bestVal = -1000
            bestMove = (0,0)
            
            if maximizing:
                node_legalMoves = node._legalMoves(self.color)
            else:
                node_legalMoves = node._legalMoves(self.opponentColor)
                
            for i in node_legalMoves:
                if maximizing:
                    branch = node.makeMove(i[0], i[1], self.color)
                else:
                    branch = node.makeMove(i[0], i[1], self.opponentColor)
                nextMove, val = self.minimax(branch, depth-1, not maximizing)
                if val > bestVal:
                    bestVal = val
                    bestMove = i
            return bestMove, -bestVal
            
class ViewingPurposes: 
    def __init__(self, model, screen, array, cell_width, cell_height):
        self.model = model 
        self.screen = screen
        self.array = array
        self.cell_width = cell_width
        self.cell_height = cell_height  
        
    def drawBoard(self, currentBoard):
        print "before screen fill" 
        self.screen.fill(pygame.Color(255,255,255)) #setting background color 
        print "after screen fill"
        rows = 8 
        columns = 8 
        for i in range(rows):
            for j in range(columns):
                cell = pygame.Rect((i*self.cell_height), (j*self.cell_width), self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, (200, 5, 156), cell)
                
        ##draw the four original circles 
        #pygame.draw.circle(Surface, color, position, radius, width)
        
        ##then while loop with updating circles 
#        for k in range(rows): 
#            for c in range(columns): 
#                center = ((k*cell_height + ((k*cell_height)/2.0)), (c*cell_height +((c*cell_height)/2.0)))
#                if #color is black
#                    pygame.draw.circle(self.screen, ())
#                elif #color is white 
#                    pygame.draw.circle(self.screen, ())
    
        
    def update(self): 
         for i in range(1,size-1):
             
            for j in range(1,size-1):
                if self.array[i][j] == white:
                    print 'W',
                elif self.array[i][j] == black:
                    print 'B',
                else:
                    pass #what do I put here? CHECK THIS LATER

class OthelloController:
    def __init__(self, model):
        self.model = model
    
    def makeMove(self, row, col, piece):
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
        
            
if __name__=='__main__':
#    '''Manages playing an actual game of Othello.'''
#    screen = pygame.display.set_mode((self.length_of_board, self.length_of_board))
#    view = ViewingPurposes(self, screen, self.array, cell_width, cell_height)

    model = OthelloBoard([], size)

    print 'Black goes first.'
    
    # Two player objects: [black, white]
    players = [None, None]
    colorNames = ('black', 'white')
    colorValues = (black, white)
    invalidPasses = [0, 0]
    illegalMoves = [0, 0]
    start_heuristic = 0

    # Determine whether each player is human or computer, and
    # instantiate accordingly
    for i in range(2):
        response = raw_input('Should ' + colorNames[i] + ' be (h)uman or (c)omputer? ')
        
        if response.lower() == 'h':
            name = raw_input("What is the player's name? ")
            players[i] = HumanPlayer(name,colorValues[i])
        else:
            plies = int(raw_input("How many plies ahead should the computer look? "))
            players[i] = ComputerPlayer('compy' + colorNames[i], colorValues[i], start_heuristic, plies)

    # Number of times a "pass" move has been made, in a row
    passes = 0

    done = False
    
    while not done:
        model.playPly(passes, done)

    # Display final outcome
    scores = self.curBoard.scores()
    if scores[0] > scores[1]:
        print 'Black wins!'
    elif scores[1] > scores[0]:
        print 'White wins!'
    else:
        print 'Tie game!!'

#    prompt = raw_input("Play? "); 
#    if prompt == "y":
#        size = (640, 640)
#        side_length = 640 #only works if square 
#        screen = pygame.display.set_mode(size)
#        white = 1
#        black = -1
#        empty = 0
#        maxDepth = 10
#        cell_width = 80 
#        cell_height = 80 
#        
#        
#        model = OthelloBoard([], side_length)
#        model.playGame()
#        view = ViewingPurposes(model,screen, model.array, cell_width, cell_height)
#        view.drawBoard(model.curBoard)
        
        
        
    