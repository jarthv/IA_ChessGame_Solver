import pyglet
from pyglet.window import mouse
import pyglet
import itertools
import chessGUI
import chess
from game import Game
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.theme import Theme
import theme
from pyglet_gui.manager import Manager
from pyglet_gui.constants import *
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.gui import Label
from pyglet_gui.containers import VerticalContainer,HorizontalContainer

from pyglet_gui.theme import Theme
from theme import getTheme





class BoardCreatorGUI(pyglet.window.Window):


    spriteimage = pyglet.resource.image('resources/spritesheet.png')
    backgroundImg = pyglet.resource.image('resources/Background.png')
    chessboard = pyglet.resource.image('resources/chessboard.png')
    chessboardInv = pyglet.resource.image('resources/chessboardflipped.png')
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
    #Flags
    whiteKingCastling = False
    whiteQueenCastling = False
    blackKingCastling = False
    blackQueenCastling = False
    CPUPlayWhite=False
    CPUStarts=False

    chessboardflipped = False




    quantityOfPieces = {"NR":0, "ND":0, "NA":0,"NC":0, "NT":0, "NP":0,"BR":0, "BD":0, "BA":0,"BC":0, "BT":0, "BP":0}

    def __init__(self,batch):
        super(BoardCreatorGUI, self).__init__(900, 600,
                                       resizable=False,
                                       caption='Chess',
                                       config=pyglet.gl.Config(double_buffer=True),
                                       vsync=False)


        self.board_imgs = [[None for _ in range(8)] for _ in range(8)]
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.selector_imgs = [None for _ in range(12)]


        self.selectedPiece = []
        self.board_normal = pyglet.sprite.Sprite(self.chessboard)
        self.board_flipped = pyglet.sprite.Sprite(self.chessboardInv)
        self.piece_held=None
        self.createStdPieces()
        self.background = pyglet.sprite.Sprite(self.backgroundImg)
        self.mouseAxis=(0,0)
        self.batch = batch
        self.managerList=[]
        self.manager()





    def manager(self):

        self.managerList+=[Manager(HorizontalContainer([OneTimeButton(label="Continuar",on_release=self.nextWindow)]),
                window=self,
                batch=self.batch,
                theme=getTheme(),
                anchor=ANCHOR_BOTTOM_RIGHT,
                offset=(-80, 5),
                is_movable=False
                )]

        self.managerList+=[Manager(VerticalContainer([Checkbox(label="El CPU Inicia        ",on_press=self.setCPUStarts,is_pressed=self.CPUStarts),
                                   Checkbox(label="El CPU es blancas", on_press=self.setCPUPlayWhite,is_pressed=self.CPUPlayWhite),
                                   Label(""),Label("Enroque de negras"),
                                   Checkbox(label="Lado de la Reina ", on_press=self.setBlackQueenCastling,is_pressed=self.blackQueenCastling),
                                   Checkbox(label="Lado del Rey       ", on_press=self.setBlackKingCastling,is_pressed=self.blackKingCastling),
                                   Label(""),Label("Enroque de blancas"),
                                   Checkbox(label="Lado de la Reina ",on_press=self.setWhiteQueenCastling,is_pressed=self.whiteQueenCastling),
                                   Checkbox(label="Lado del Rey       ", on_press=self.setWhiteKingCastling,is_pressed=self.whiteKingCastling)
                                   ]),
                window=self,
                batch=self.batch,
                theme=getTheme(),
                anchor=ANCHOR_RIGHT,
                offset=(-50, -95),
                is_movable=False
                )]

    def setWhiteKingCastling(self,y):
        self.whiteKingCastling=y;
    def setWhiteQueenCastling(self,y):
        self.whiteQueenCastling=y;
    def setBlackKingCastling(self,y):
        self.blackKingCastling=y;
    def setBlackQueenCastling(self,y):
        self.blackQueenCastling=y;
    def setCPUPlayWhite(self,y):
        self.CPUPlayWhite=y;
    def setCPUStarts(self,y):
        self.CPUStarts=y;


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
    def ifFlipped(self, x):
        if(self.CPUPlayWhite):
            return (7-x)
        return x
    def deleteManagers(self):
        for x in self.managerList:
            x.delete()

    def on_draw(self):
        self.clear()

        self.background.draw()
        if(self.CPUPlayWhite):
            self.board_flipped.draw()
        else:
            self.board_normal.draw()


        for n in self.selector_imgs:
            if(n!= None):
                n.draw()

        for x, y in itertools.product(range(8), repeat=2):
            if self.board[y][x] != "":
                piece = self.board_imgs[y][x]

                if piece != self.piece_held:
                    piece.x = self.ifFlipped(x) * 75
                    piece.y = self.ifFlipped(y) * 75
                piece.draw()
        if(self.newPiece):
            self.piece_held.draw()

        x = self.mouseAxis[0]
        y = self.mouseAxis[1]
        self.batch.draw()


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
            self.old_pos=(self.ifFlipped(x//75),self.ifFlipped(y//75))

            return self.board_imgs[self.ifFlipped(y//75)][self.ifFlipped(x//75)]

    def on_mouse_motion(self,x, y, dx, dy):
        self.mouseAxis = (x,y)

    def on_mouse_press(self,x, y, button, modifiers):
        if button == mouse.LEFT :
            piece = self.getGraphicPiece(x, y)
            if piece != None:
                if(not self.newPiece):
                    self.piece_heldId = self.board[self.ifFlipped(y//75)][self.ifFlipped(x//75)]
                self.piece_held = piece



    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if self.piece_held is not None:
            self.piece_held.x = x - 32
            self.piece_held.y = y - 32

    def nextWindow(self,y):
        castling=""
        starts = "w"
        if(self.whiteKingCastling):
            castling += "K"

        if(self.whiteQueenCastling):
            castling += "Q"

        if (self.blackKingCastling):
            castling += "k"

        if (self.blackQueenCastling):
            castling += "q"

        if(self.CPUStarts):
            starts="b"
        if(self.CPUPlayWhite):
            if(starts == "b"):
                starts="w"
            elif starts=="w":
                starts = "b"
        if(castling == ""):
            castling="-"
        batch = pyglet.graphics.Batch()
        mygame = chessGUI.ChessGUI(self.boardTraduction(),castling,starts,self.CPUPlayWhite,self,batch)
        self.set_visible(False)


    def on_mouse_release(self,x, y, button, modifiers):
        if self.piece_held is not None and (x > 600 or not self.newPiece) and self.old_pos != (-1,-1):
            self.board_imgs[self.old_pos[1]][self.old_pos[0]] = None
            if(self.board[self.old_pos[1]][self.old_pos[0]] == "BR"):
                self.whiteKingOnBoard = False
            elif (self.board[self.old_pos[1]][self.old_pos[0]] == "NR"):
                self.blackKingOnBoard = False
            self.board[self.old_pos[1]][self.old_pos[0]] = ""

        if self.piece_held is not None and (x<=600):
            xp = self.ifFlipped(x//75)
            yp = self.ifFlipped(y // 75)
            if (self.board[yp][xp] == "BR"):
                self.whiteKingOnBoard = False
            elif (self.board[yp][xp] == "NR"):
                self.blackKingOnBoard = False
            self.board_imgs[yp][xp] = self.piece_held
            self.board[yp][xp] = self.piece_heldId

            if (self.piece_heldId == "BR"):
                self.whiteKingOnBoard = True
            elif (self.piece_heldId == "NR"):
                self.blackKingOnBoard = True


        self.piece_held = None
        self.old_pos=(-1,-1)
        self.piece_heldId = ""
        self.newPiece= False
        self.createStdPieces()
    def boardTraduction(self):
        resultBoard=[]
        for x in range(8):
            for y in range(8):
                if(self.board[y][x] != ""):
                    resultBoard += [self.board[y][x] +self.colPositions[x] + str(y+1)]
        return resultBoard


