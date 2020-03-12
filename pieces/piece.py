import pyglet
import time

spriteimage = pyglet.resource.image('resources/spritesheet.png')
spritesheet = pyglet.image.ImageGrid(spriteimage, 2, 6)
dangerImg = pyglet.resource.image('resources/danger.png')
BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, \
WHITE_KNIGHT, WHITE_ROOK, WHITE_PAWN = range(12)


class Piece(object):
    white = True
    piecesprite = None
    captured = False
    xMovement=0
    yMovement=0

    def __init__(self, type):
        self.white = type
        self.captured = False
        pyglet.clock.schedule_interval(self.updatePosition,1/100)

    def MakeMove(self, board, move, king):
        x = int(self.piecesprite.x // 75)
        y = int(self.piecesprite.y // 75)
        temp = board[y][x]
        temp2 = board[move[0]][move[1]]
        board[move[0]][move[1]] = board[y][x]
        board[y][x] = None
        check = king.InCheck(board)
        board[move[0]][move[1]] = temp2
        board[y][x] = temp
        return check
    
    def updatePosition(self,dt):
        stepSize=15
        if(self.yMovement>0):
            if(self.yMovement <= stepSize):
                self.piecesprite.y += self.yMovement
                self.yMovement = 0
            else:
                self.piecesprite.y += stepSize
                self.yMovement -= stepSize
        if(self.yMovement<0):
            if(self.yMovement >= -stepSize):
                self.piecesprite.y += self.yMovement
                self.yMovement = 0
            else:
                self.piecesprite.y -= stepSize
                self.yMovement += stepSize
        if(self.xMovement>0):
            if(self.xMovement <= stepSize):
                self.piecesprite.x += self.xMovement
                self.xMovement = 0
            else:
                self.piecesprite.x += stepSize
                self.xMovement -= stepSize
        if(self.xMovement<0):
            if(self.xMovement >= -stepSize):
                self.piecesprite.x += self.xMovement
                self.xMovement = 0
            else:
                self.piecesprite.x -= stepSize
                self.xMovement += stepSize



    def GetValidMoves(self, board, king):
        ListOfMoves = self.GetThreatSquares(board)
        ValidMoves = []
        for move in ListOfMoves:
            # tempboard = deepcopy(board)                                         # Can be optimized. Edit MakeMove function to simply revert any changes
            if not self.MakeMove(board, move, king):
                ValidMoves.append(move)
        return ValidMoves


 
    def ChangeLocation(self, x, y, board):
        endX = x*75
        endY= y*75
        startX= self.piecesprite.x
        startY = self.piecesprite.y
        self.xMovement = endX - startX
        self.yMovement = endY - startY

        
  

    def Draw(self):
        self.piecesprite.draw()

