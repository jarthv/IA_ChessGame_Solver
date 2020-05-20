import pyglet
from pyglet.window import mouse
import pyglet
import itertools
import chessGUI
import chess
from game import Game




class BoardCreatorGUI(pyglet.window.Window):


    spriteimage = pyglet.resource.image('resources/spritesheet.png')
    backgroundImg = pyglet.resource.image('resources/Background.png')
    chessboard = pyglet.resource.image('resources/chessboard.png')
    continueBimg = pyglet.resource.image('resources/continueB.png')
    continueNimg = pyglet.resource.image('resources/continueN.png')

    spritesheet = pyglet.image.ImageGrid(spriteimage, 2, 6)
    BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, \
    WHITE_KNIGHT, WHITE_ROOK, WHITE_PAWN = range(12)
    piecesIds=["NR", "ND", "NA","NC", "NT", "NP","BR", "BD", "BA","BC", "BT", "BP"]

    dictPieces = {"NR": spritesheet[BLACK_KING], "ND": spritesheet[BLACK_QUEEN], "NA": spritesheet[BLACK_BISHOP],
            "NC": spritesheet[BLACK_KNIGHT], "NT": spritesheet[BLACK_ROOK], "NP": spritesheet[BLACK_PAWN],
            "BR": spritesheet[WHITE_KING], "BD": spritesheet[WHITE_QUEEN], "BA": spritesheet[WHITE_BISHOP],
            "BC": spritesheet[WHITE_KNIGHT], "BT": spritesheet[WHITE_ROOK], "BP": spritesheet[WHITE_PAWN]}

    # ["BTf1", "NTe7", "BAd5", "BRd6", "NRd8"]
    colPositions = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h" }
    colPositionsInv = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    stdChesBoard = ["NTh1", "NAh3", "NCh2", "NDh4", "NRh5", "NTh8", "NAh6", "NCh7",
                    "NPg1", "NPg2", "NPg3", "NPg4", "NPg5", "NPg6", "NPg7", "NPg8",
                    "BPb1", "BPb2", "BPb3", "BPb4", "BPb5", "BPb6", "BPb7", "BPb8",
                    "BTa1", "BAa3", "BCa2", "BDa4", "BRa5", "BTa8", "BAa6", "BCa7"]
    testCastling = ["NTh1", "NRh5", "NTh8",
                    "NPg1", "NPb3", "NPg5", "NPg7",
                    "BPb7", "BPg2", "BPb6", "BPb8",
                    "BTa1", "BRa5", "BTa8",]
    spanishToEnglish = {"A": "B", "T": "R", "D": "Q", "R": "K", "P": "P", "C": "N"}
    englishToSpanish = {"B": "A", "R": "T", "Q": "D", "K": "R", "P": "P", "N": "C"}
    turn="B"
    playerTurn="B"
    ia_mode=False
    blackKing=None
    whiteKing=None
    promotion= False
    promotionMov=[]
    promotedPiece=""
    piece_held =  None
    piece_heldId=""
    old_pos=(-1,-1)
    newPiece=False
    blackKingOnBoard=False
    whiteKingOnBoard = False


    quantityOfPieces = {"NR":0, "ND":0, "NA":0,"NC":0, "NT":0, "NP":0,"BR":0, "BD":0, "BA":0,"BC":0, "BT":0, "BP":0}

    def __init__(self):
        super(BoardCreatorGUI, self).__init__(900, 600,
                                       resizable=False,
                                       caption='Chess',
                                       config=pyglet.gl.Config(double_buffer=True),
                                       vsync=False)
        self.board_imgs = [[None for _ in range(8)] for _ in range(8)]
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.selector_imgs = [None for _ in range(12)]

        self.continueB = pyglet.sprite.Sprite(self.continueBimg)
        self.continueN = pyglet.sprite.Sprite(self.continueNimg)

        self.selectedPiece = []
        self.board_normal = pyglet.sprite.Sprite(self.chessboard)
        self.piece_held=None
        self.createStdPieces()
        self.background = pyglet.sprite.Sprite(self.backgroundImg)
        self.mouseAxis=(0,0)


    def createStdPieces(self):
        for n in range(12):
            if(self.selector_imgs[n] == None):
                if(self.whiteKingOnBoard and n == 6 or self.blackKingOnBoard and n == 0  ):
                    continue
                else:
                    self.selector_imgs[n]=pyglet.sprite.Sprite(self.spritesheet[n],75*(8+n//3),75*(5+((11-n)%3)))



    def endOfTurn(self):
        if(self.turn=="B"):
            self.turn = "N"
        else:
            self.turn = "B"

    def on_draw(self):
        self.clear()

        self.background.draw()
        self.board_normal.draw()

        for n in self.selector_imgs:
            if(n!= None):
                n.draw()

        for x, y in itertools.product(range(8), repeat=2):
            if self.board[y][x] != "":
                piece = self.board_imgs[y][x]

                if piece != self.piece_held:
                    piece.x = x * 75
                    piece.y = y * 75
                piece.draw()
        if(self.newPiece):
            self.piece_held.draw()

        x = self.mouseAxis[0]
        y = self.mouseAxis[1]

        if (x <= 846.5 and x >= 635.5 and y <= 84 and y >= 42):
            self.continueB.x = 635.5
            self.continueB.y = 42
            self.continueB.draw()
        else:
            self.continueN.x=635.5
            self.continueN.y = 42
            self.continueN.draw()


#193 42


    def getGraphicPiece(self,x,y):
        if(x>600 and y>375):
            xc = x//75 - 8
            yc = y//75 - 5
            result = self.selector_imgs[xc*3 + (2-yc)]
            if(result != None):
                self.selector_imgs[xc * 3 + (2-yc)] = None
                self.newPiece =True
                self.piece_heldId =self.piecesIds[ xc*3 + (2-yc)]
            return result

        elif(x<=600):
            self.old_pos=(x//75,y//75)

            return self.board_imgs[y//75][x//75]

    def on_mouse_motion(self,x, y, dx, dy):
        self.mouseAxis = (x,y)
        print(self.mouseAxis)

    def on_mouse_press(self,x, y, button, modifiers):
        if button == mouse.LEFT :
            piece = self.getGraphicPiece(x, y)
            if piece != None:
                if(not self.newPiece):
                    self.piece_heldId = self.board[y//75][x//75]
                self.piece_held = piece



    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if self.piece_held is not None:
            self.piece_held.x = x - 32
            self.piece_held.y = y - 32



    def on_mouse_release(self,x, y, button, modifiers):
        if self.piece_held is not None and (x > 600 or not self.newPiece):
            self.board_imgs[self.old_pos[1]][self.old_pos[0]] = None
            if(self.board[self.old_pos[1]][self.old_pos[0]] == "BR"):
                self.whiteKingOnBoard = False
            elif (self.board[self.old_pos[1]][self.old_pos[0]] == "NR"):
                self.blackKingOnBoard = False
            self.board[self.old_pos[1]][self.old_pos[0]] = ""

        if self.piece_held is not None and (x<=600):
            if (self.board[y//75][x//75] == "BR"):
                self.whiteKingOnBoard = False
            elif (self.board[y//75][x//75] == "NR"):
                self.blackKingOnBoard = False
            self.board_imgs[y//75][x//75] = self.piece_held
            self.board[y//75][x//75] = self.piece_heldId

            if (self.piece_heldId == "BR"):
                self.whiteKingOnBoard = True
            elif (self.piece_heldId == "NR"):
                self.blackKingOnBoard = True
        if (x <= 846.5 and x >= 635.5 and y <= 84 and y >= 42):
            mygame = chessGUI.ChessGUI(self.boardTraduction(),self)
            self.set_visible(False)


        self.piece_held = None
        self.old_pos=(-1,-1)
        self.piece_heldId = ""
        self.newPiece= False
        self.createStdPieces()
        # print(self.board)
    def boardTraduction(self):
        resultBoard=[]
        for x in range(8):
            for y in range(8):
                if(self.board[y][x] != ""):
                    resultBoard += [self.board[y][x] +  self.colPositions[x] + str(y+1) ]
        print(resultBoard)
        return resultBoard


