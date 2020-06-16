import pyglet
from pyglet.window import mouse
import pyglet
import itertools
import chess
from game import Game
import time
from theme import getTheme, getPopUpMenssageTheme
from pyglet_gui.manager import Manager
from pyglet_gui.document import Document
from pyglet_gui.constants import *
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.gui import Label, PopupMessage, Frame
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from datetime import datetime
import easygui

#
#
#
#
# La salida de archivo será la posición inicial de las piezas con la descripción
# algebráica de la partida efectuada, y una indicación de fecha y tiempo (un time-stamp de la
# solución).
#


class ChessGUI(pyglet.window.Window):

    chessboard = pyglet.resource.image('resources/chessboard.png')
    chessboardInv = pyglet.resource.image('resources/chessboardflipped.png')
    validImg = pyglet.resource.image('resources/validmove.png')
    promoImg = pyglet.resource.image('resources/promotion.png')
    hoverImg = pyglet.resource.image('resources/hoversquare.png')
    spriteimage = pyglet.resource.image('resources/spritesheet.png')
    dangerImg = pyglet.resource.image('resources/danger.png')

    backgroundImg = pyglet.resource.image('resources/Background.png')

    spritesheet = pyglet.image.ImageGrid(spriteimage, 2, 6)
    BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK, BLACK_PAWN, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, \
        WHITE_KNIGHT, WHITE_ROOK, WHITE_PAWN = range(12)

    dictPieces = {"NR": spritesheet[BLACK_KING], "ND": spritesheet[BLACK_QUEEN], "NA": spritesheet[BLACK_BISHOP],
                  "NC": spritesheet[BLACK_KNIGHT], "NT": spritesheet[BLACK_ROOK], "NP": spritesheet[BLACK_PAWN],
                  "BR": spritesheet[WHITE_KING], "BD": spritesheet[WHITE_QUEEN], "BA": spritesheet[WHITE_BISHOP],
                  "BC": spritesheet[WHITE_KNIGHT], "BT": spritesheet[WHITE_ROOK], "BP": spritesheet[WHITE_PAWN]}

    # ["BTf1", "NTe7", "BAd5", "BRd6", "NRd8"]
    colPositions = {"a": 0, "b": 1, "c": 2,
                    "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colPositionsInv = {"a": 0, "b": 1, "c": 2,
                       "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    stdChesBoard = ["NTa8", "NCb8", "NAc8",  "NDd8", "NRe8", "NAf8", "NCg8", "NTh8",
                    "NPa7", "NPb7", "NPc7", "NPd7", "NPe7", "NPf7", "NPg7",  "NPh7",
                    "BPa2", "BPb2", "BPc2", "BPd2", "BPe2", "BPf2", "BPg2",  "BPh2",
                    "BTa1", "BCb1", "BAc1",  "BDd1", "BRe1", "BAf1", "BCg1", "BTh1", ]

    spanishToEnglish = {"A": "B", "T": "R",
                        "D": "Q", "R": "K", "P": "P", "C": "N"}
    englishToSpanish = {"B": "A", "R": "T",
                        "Q": "D", "K": "R", "P": "P", "N": "C"}
    ia_mode = True
    blackKing = None
    whiteKing = None
    promotion = False
    promotionMov = []
    promotedPiece = ""
    movement = [0, 0]
    animation = True

    def __init__(self, textPositions, castlingRigths, starts, CPUPlaysWhite, pwindow, batch):
        super(ChessGUI, self).__init__(900, 600,
                                       resizable=False,
                                       caption='Chess',
                                       config=pyglet.gl.Config(
                                           double_buffer=True),
                                       vsync=False)
        pyglet.clock.schedule_interval(self.updatePosition, 1 / 60)
        self.board_imgs = [[None for _ in range(8)] for _ in range(8)]
        self.board = []
        self.window = pwindow
        self.batch = batch

        self.CPUPlaysWhite = CPUPlaysWhite
        self.castlingRigths = castlingRigths
        self.starts = starts

        if(starts == "b"):
            self.turn = "N"
        else:
            self.turn = "B"
        if CPUPlaysWhite:
            self.playerTurn = "N"
        else:
            self.playerTurn = "B"

        self.selectedPiece = []
        self.board_normal = pyglet.sprite.Sprite(self.chessboard)
        self.board_flipped = pyglet.sprite.Sprite(self.chessboardInv)
        self.hoverSprite = pyglet.sprite.Sprite(self.hoverImg)
        self.danger = pyglet.sprite.Sprite(self.dangerImg)
        self.piece_held = None
        self.textPositions = textPositions

        self.createBoard(textPositions)
        self.inFunction = False
        self.draws = 0

        self.game = Game(self.stdNotationToChess(self.board) +
                         " "+starts+" "+castlingRigths+" - 0 1")
        self.wQueen = pyglet.sprite.Sprite(self.spritesheet[7], 131.25, 225)
        self.wRook = pyglet.sprite.Sprite(self.spritesheet[10], 218.75, 225)
        self.wBishop = pyglet.sprite.Sprite(self.spritesheet[8], 306.25, 225)
        self.wKnight = pyglet.sprite.Sprite(self.spritesheet[9], 393.75, 225)
        self.bQueen = pyglet.sprite.Sprite(self.spritesheet[1], 131.25, 225)
        self.bRook = pyglet.sprite.Sprite(self.spritesheet[4], 218.75, 225)
        self.bBishop = pyglet.sprite.Sprite(self.spritesheet[2], 306.25, 225)
        self.bKnight = pyglet.sprite.Sprite(self.spritesheet[3], 393.75, 225)
        self.background = pyglet.sprite.Sprite(self.backgroundImg)
        self.document = Document(pyglet.text.decode_attributed(
            "\n"*23), width=250, height=400)
        self.manager()
        self.numero = 0
        self.announcedFinal = False
        self.instanteInicial = None
        self.instanteFinal = None
        self.lineCont = 1
        self.annotations = ""

    def manager(self):
        Manager(Label(""),
                window=self, batch=self.batch,
                theme=getTheme()
                )
        Manager(Frame(self.document),
                window=self, batch=self.batch,
                theme=getTheme(),
                anchor=ANCHOR_TOP_RIGHT,
                offset=(-10, -75),
                is_movable=False
                )
        Manager(HorizontalContainer([OneTimeButton(label="Guardar", on_release=self.saveGame), OneTimeButton(label="Volver", on_release=self.onclose)]),
                window=self,
                batch=self.batch,
                theme=getTheme(),
                anchor=ANCHOR_BOTTOM_RIGHT,
                offset=(-50, 15),
                is_movable=False
                )
        self.document.set_text("")

    def updateDocument(self, y):
        self.numero += 1
        self.document.set_text(self.document.get_text() +
                               "Hola Mundos "+str(self.numero)+"\n")
        self.popupMessage("Partida guardada correctamente")

    def popupMessage(self, text):
        PopupMessage(text=text,
                     window=self,
                     batch=self.batch,
                     theme=getPopUpMenssageTheme()
                     )

    def saveGame(self, y):
        result = "{\n\tPosicionInicial: " + str(self.textPositions) + ",\n"
        result += "\tDesarrolloDeLaPartida: \"" + self.annotations+"\",\n"
        date = datetime.now().strftime("%d/%m/%Y")
        fileDate = datetime.now().strftime("%d-%m-%Y")
        result += "\tfecha: \""+date+"\",\n"
        strTiempo = "null"
        if not (self.instanteInicial == None or self.instanteFinal == None):
            tiempo = (self.instanteFinal-self.instanteInicial)
            strTiempo = str(tiempo)
        result += "\ttiempo: \"" + strTiempo+"\" \n}"
        fileroute = easygui.filesavebox(default="BotFinalesDeAjedrez " + fileDate +
                                        ".txt", msg="hola", title="Seleccione el destino", filetypes="txt")
        if(fileroute != None):
            f = open(fileroute, "w")
            f.write(result)
            f.close()

    def stdNotationToChess(self, boardGUI):
        count = 0
        result = ""
        row = ""
        for x in range(8):
            if (result != ""):
                result += "/"
            for y in range(8):
                if boardGUI[x][y] == "":
                    count += 1
                else:
                    charName = self.spanishToEnglish[boardGUI[x][y][1]]
                    if (boardGUI[x][y][0] == "N"):
                        charName = charName.lower()
                    if count != 0:
                        row += str(count) + charName
                        count = 0
                    else:
                        row += charName
            if count != 0:
                row += str(count)
                count = 0
            result += row[::-1]
            row = ""

        return result[::-1]

    def endOfTurn(self):
        if (self.turn == "B"):
            self.turn = "N"
        else:
            self.turn = "B"

    def moveOfAI(self):
        var = str(self.game.suggestedMove(self.turn))
        xi = self.colPositions[var[0]]
        yi = int(var[1]) - 1
        xf = self.colPositions[var[2]]
        yf = int(var[3]) - 1
        piece = ""
        if(len(var) == 5):
            piece = self.englishToSpanish[var[4].upper()]
        self.pieceMove(xi, yi, xf, yf, piece)

    def ifIsFlipped(self, x):
        if(self.CPUPlaysWhite):
            return (7-x)
        return x

    def promote(self):
        self.promoImg.blit(100, 200)
        if self.turn == "N":
            self.bQueen.draw()
            self.bRook.draw()
            self.bBishop.draw()
            self.bKnight.draw()
        else:
            self.wQueen.draw()
            self.wRook.draw()
            self.wBishop.draw()
            self.wKnight.draw()

    def createBoard(self, textPositions) -> list:

        self.board = [["" for i in range(8)] for i in range(8)]
        if textPositions:
            for i in textPositions:
                y = ord(i[2])-97
                x = int(i[3]) - 1
                p = i[0] + i[1]

                self.board[self.ifIsFlipped(x)][self.ifIsFlipped(y)] = p

                self.board_imgs[self.ifIsFlipped(x)][self.ifIsFlipped(
                    y)] = pyglet.sprite.Sprite(self.dictPieces[p])
                if (p == "BR"):
                    self.whiteKing = self.board_imgs[self.ifIsFlipped(
                        x)][self.ifIsFlipped(y)]
                elif(p == "NR"):
                    self.blackKing = self.board_imgs[self.ifIsFlipped(
                        x)][self.ifIsFlipped(y)]

    def onclose(self, y):
        self.window.set_visible(True)
        self.window.deleteManagers()
        self.window.manager()
        self.close()

    def on_draw(self):
        self.clear()
        self.background.draw()
        if(self.CPUPlaysWhite):
            self.board_flipped.draw()
        else:
            self.board_normal.draw()
        if(self.game.isCheck()):
            if(self.turn == "B"):
                self.danger.x = self.whiteKing.x
                self.danger.y = self.whiteKing.y
            else:
                self.danger.x = self.blackKing.x
                self.danger.y = self.blackKing.y
            self.danger.draw()

        if self.selectedPiece != []:
            self.hoverSprite.x = (self.selectedPiece[1] // 75) * 75
            self.hoverSprite.y = (self.selectedPiece[2] // 75) * 75
            self.hoverSprite.draw()

        for x, y in itertools.product(range(8), repeat=2):
            if self.board[y][x] != "":
                piece = self.board_imgs[y][x]

                if piece != self.piece_held:
                    piece.x = x * 75
                    piece.y = y * 75
                    piece.draw()
        if(self.piece_held != None):
            self.piece_held.draw()

        self.announceFinal()

        if(self.promotion):
            self.promote()

        if(self.draws < 60):
            self.draws += 1
        self.batch.draw()

    def announceFinal(self):
        if(self.instanteInicial == None):
            self.instanteInicial = datetime.now()
        if (self.game.isCheckMate() and not self.announcedFinal and self.draws == 60):
            self.announcedFinal = True
            self.instanteFinal = datetime.now()
            if (self.turn == "B"):
                self.popupMessage("Jaque mate de las piezas negras")
            if (self.turn == "N"):
                self.popupMessage("Jaque mate de las piezas blancas")
        if (self.game.isStalemate() and not self.announcedFinal and self.draws == 60):
            self.announcedFinal = True
            self.instanteFinal = datetime.now()
            self.popupMessage("Empate")

    def pieceMove(self, xi, yi, xf, yf, piece=""):
        fromSquare = chr(xi + 97) + str(1 + yi)
        toSquare = chr(xf + 97) + str(1 + yf)
        pieceEng = ""
        if(piece != ""):
            self.board[yi][xi] = self.board[yi][xi][0] + piece
            ximg = self.board_imgs[yi][xi].x
            yimg = self.board_imgs[yi][xi].y
            self.board_imgs[yi][xi] = pyglet.sprite.Sprite(
                self.dictPieces[self.board[yi][xi]])
            self.board_imgs[yi][xi].x = ximg
            self.board_imgs[yi][xi].y = yimg

            pieceEng = self.spanishToEnglish[piece].lower()

        result = self.game.doAMove(fromSquare + toSquare + pieceEng)

        if (result[0] != ""):
            self.changePosition(xi, yi, xf, yf)
            if (result[0] == "PassantMove"):
                self.doPassant(xi, yi, xf, yf)

            elif(result[0] == "kingside" or result[0] == "queenside"):
                self.doCastling(result[0], yi, yf)
            self.anotateMove(result[1])
            self.endOfTurn()

    def anotateMove(self, move):
        result = ""
        if(self.turn == "N"):
            if(self.lineCont == 1 and self.annotations == ""):
                result += "1...  "+move+" "
            else:
                result += "  "+move+" "
            self.lineCont += 1

        elif(self.turn == "B"):
            result += str(self.lineCont)+". " + move
        self.annotations += result

        newLine = "\n"
        if(self.turn == "N"):
            newLine = ""
        self.document.set_text(self.document.get_text()+newLine + result)

    def changePosition(self, xi, yi, xf, yf):
        self.board_imgs[yf][xf] = self.board_imgs[yi][xi]
        self.board_imgs[yi][xi] = None
        self.board[yf][xf] = self.board[yi][xi]
        self.board[yi][xi] = ""
        if self.animation:
            self.piece_held = self.board_imgs[yf][xf]
            xmovement = xf*75 - xi*75
            ymovement = yf*75 - yi*75
            self.movement = [xmovement, ymovement]

    def updatePosition(self, dt):
        if(len(self.movement) == 2 and self.piece_held != None):
            stepSize = 10
            if (self.movement[1] > 0):
                if (self.movement[1] <= stepSize):
                    self.piece_held.y += self.movement[1]
                    self.movement[1] = 0
                else:
                    self.piece_held.y += stepSize
                    self.movement[1] -= stepSize
            if (self.movement[1] < 0):
                if (self.movement[1] >= -stepSize):
                    self.piece_held.y += self.movement[1]
                    self.movement[1] = 0
                else:
                    self.piece_held.y -= stepSize
                    self.movement[1] += stepSize
            if (self.movement[0] > 0):
                if (self.movement[0] <= stepSize):
                    self.piece_held.x += self.movement[0]
                    self.movement[0] = 0
                else:
                    self.piece_held.x += stepSize
                    self.movement[0] -= stepSize
            if (self.movement[0] < 0):
                if (self.movement[0] >= -stepSize):
                    self.piece_held.x += self.movement[0]
                    self.movement[0] = 0
                else:
                    self.piece_held.x -= stepSize
                    self.movement[0] += stepSize

            if(self.movement[0] == 0 and self.movement[1] == 0):
                self.piece_held = None
                self.movement = []
        if (self.turn != self.playerTurn and self.ia_mode and not self.game.isCheckMate() and not self.game.isStalemate() and self.piece_held == None and not self.inFunction and self.draws == 60):
            self.inFunction = True
            self.moveOfAI()
            self.turn = self.playerTurn
            self.inFunction = False

    def doCastling(self, side, yi, yf):
        if(side == "kingside"):
            self.changePosition(7, yi, 5, yf)
        if(side == "queenside"):
            self.changePosition(0, yi, 3, yf)

    def doPassant(self, xi, yi, xf, yf):
        if (self.turn == "B"):
            self.board_imgs[yf - 1][xf] = None
            self.board[yf - 1][xf] = ""
        if (self.turn == "N"):
            self.board_imgs[yf + 1][xf] = None
            self.board[yf + 1][xf] = ""

    def isPromote(self, yf):
        result = False
        if(self.selectedPiece[0] == "BP" and self.selectedPiece[2]//75 == 6 and yf == 7):
            result = True
        elif(self.selectedPiece[0] == "NP" and self.selectedPiece[2]//75 == 1 and yf == 0):
            result = True
        return result

    def on_mouse_press(self, x, y, button, modifiers):
        if(self.playerTurn == self.turn or not self.ia_mode) and not self.game.isCheckMate() and x <= 600 and y <= 600:
            if(not self.promotion):
                if self.selectedPiece != []:
                    if(((self.board[y // 75][x // 75] == "")) or (self.board[y // 75][x // 75] != "") and (self.board[y // 75][x // 75][0] != self.turn)):
                        xi = self.selectedPiece[1] // 75
                        yi = self.selectedPiece[2] // 75
                        xf = x // 75
                        yf = y // 75
                        if(self.isPromote(yf)):
                            self.promotion = True
                            self.promotionMov = [xi, yi, xf, yf]
                        else:
                            self.pieceMove(xi, yi, xf, yf)

                        self.selectedPiece = []

                if (self.board[y // 75][x // 75] != "") and (self.board[y // 75][x // 75][0] == self.turn):
                    self.selectedPiece = [
                        self.board[y // 75][x // 75]] + [x, y]
            else:
                if 225 < y < 300:
                    xi = self.promotionMov[0]
                    yi = self.promotionMov[1]
                    xf = self.promotionMov[2]
                    yf = self.promotionMov[3]
                    piece = ""
                    if 131.25 < x < 206.25:  # queen
                        piece = "D"
                    elif 218.75 < x < 293.75:  # rook
                        piece = "T"
                    elif 306.25 < x < 381.25:  # bishop
                        piece = "A"
                    elif 393.75 < x < 468.75:  # knight
                        piece = "C"
                    self.pieceMove(xi, yi, xf, yf, piece)
                    self.promotion = False
                    self.promotionFinalPos = []
