import pyglet
from pyglet.window import mouse
from chessPiecesReader import ChessPiecesReader
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.pawn import Pawn
from pieces.rook import Rook


class Chess(pyglet.window.Window):
    chessboard = pyglet.resource.image('resources/chessboard.png')
    validImg = pyglet.resource.image('resources/validmove.png')
    title = pyglet.text.Label(
        'Movimientos',
        font_name='Times New Roman',
        font_size=16,
        x=805,
        y=570,
        anchor_y='center',
        anchor_x='center',
        bold=True
    )
    promoImg = pyglet.resource.image('resources/promotion.png')
    currentPos = (-1, -1)
    move = True
    promotion = False
    spriteimage = pyglet.resource.image('resources/spritesheet.png')
    spritesheet = pyglet.image.ImageGrid(spriteimage, 2, 6)

    def __init__(self, path):
        super(Chess, self).__init__(1000, 625,
                                    resizable=False,
                                    caption='Chess',
                                    config=pyglet.gl.Config(double_buffer=True),
                                    vsync=False)

        result = ChessPiecesReader().readFile(path)

        self.wKing = result[1]
        self.bKing = result[2]
        self.board = result[0]
        self.tBoard = self.myDeepcopy(self.board)
        self.validsprites = []
        self.movs = []
        self.colPositions = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}

        self.text_moves = pyglet.text.Label(
            '',
            font_name="Comic Sans",
            font_size=12,
            x=630,
            y=500,
            multiline=True,
            width=330,
            height=495
        )

        for i in range(8):
            rowsprites = []
            for j in range(8):
                sprite = pyglet.sprite.Sprite(self.validImg, 75 * j, 75 * i)
                sprite.visible = False
                rowsprites.append(sprite)
            self.validsprites.append(rowsprites)
        self.wQueen = pyglet.sprite.Sprite(self.spritesheet[7],  131.25, 225)
        self.wRook = pyglet.sprite.Sprite(self.spritesheet[10],  218.75, 225)
        self.wBishop = pyglet.sprite.Sprite(self.spritesheet[8], 306.25, 225)
        self.wKnight = pyglet.sprite.Sprite(self.spritesheet[9], 393.75, 225)
        self.bQueen = pyglet.sprite.Sprite(self.spritesheet[1],  131.25, 225)
        self.bRook = pyglet.sprite.Sprite(self.spritesheet[4],   218.75, 225)
        self.bBishop = pyglet.sprite.Sprite(self.spritesheet[2], 306.25, 225)
        self.bKnight = pyglet.sprite.Sprite(self.spritesheet[3], 393.75, 225)

    def on_draw(self):
        self.clear()
        self.chessboard.blit(0,0)
        self.title.draw()
        self.text_moves.draw()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    self.board[i][j].Draw()
                self.validsprites[i][j].draw()
        if self.promotion:
            self.promoImg.blit(100, 200)
            if self.move:
                self.bQueen.draw()
                self.bRook.draw()
                self.bBishop.draw()
                self.bKnight.draw()
            else:
                self.wQueen.draw()
                self.wRook.draw()
                self.wBishop.draw()
                self.wKnight.draw()

    def myDeepcopy(self, copiado):
        n = len(copiado)
        mat = []
        for i in range(n):
            row = []
            for j in range(n):
                row += [None]
            mat += [row]
        i = 0
        j = 0
        while i < n:
            while j < n:
                if copiado[i][j] is not None:
                    mat[i][j] = copiado[i][j].getPtype()
                j += 1
            i += 1
            j = 0
        return mat

    def getLastMove(self):
        self.movs = []
        new = self.myDeepcopy(self.board)
        old = self.tBoard
        n = len(new)
        for i in range(n):
            for j in range(n):
                if old[i][j] != new[i][j]:
                    self.movs += [[i, j]]
        if new[self.movs[0][0]][self.movs[0][1]] is None:
            t_str = self.board[self.movs[-1][0]][self.movs[-1][1]].getPtype()
            t_str += ' to ' + self.colPositions[self.movs[-1][1]] + str(self.movs[-1][0] + 1)
            self.text_moves.text += t_str + '\n'
            self.tBoard = new
        else:
            t_str = self.board[self.movs[0][0]][self.movs[0][1]].getPtype()
            t_str += ' to ' + self.colPositions[self.movs[0][1]] + str(self.movs[0][0] + 1)
            self.text_moves.text += t_str + '\n'
            self.tBoard = new

    def on_mouse_press(self, x, y, button, modifiers):
        if self.promotion:
            if button == mouse.LEFT:
                if 225 < y < 300:
                    if 131.25 < x < 206.25:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = Queen(self.promoPawn[1], self.promoPawn[0],
                                                                                 not self.move)
                    elif 218.75 < x < 293.75:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = Rook(self.promoPawn[1], self.promoPawn[0],
                                                                                not self.move)
                    elif 306.25 < x < 381.25:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = Bishop(self.promoPawn[1], self.promoPawn[0],
                                                                                  not self.move)
                    elif 393.75 < x < 468.75:
                        self.board[self.promoPawn[0]][self.promoPawn[1]] = Knight(self.promoPawn[1], self.promoPawn[0],
                                                                                  not self.move)
                self.promoPawn = (-1, -1)
                self.promotion = False
                if not self.move:
                    if self.bKing.NoValidMoves(self.board) and not self.bKing.InCheck(self.board):
                        print('Stalemate!')
                    if self.bKing.InCheck(self.board):
                        self.bKing.danger.visible = True
                        if self.bKing.NoValidMoves(self.board):
                            print("Checkmate! White wins.")
                    if self.wKing.danger.visible:
                        if not self.wKing.InCheck(self.board):
                            self.wKing.danger.visible = False
                else:
                    if self.wKing.NoValidMoves(self.board) and not self.wKing.InCheck(self.board):
                        print('Stalemate!')
                    if self.wKing.InCheck(self.board):
                        self.wKing.danger.visible = True
                        if self.wKing.NoValidMoves(self.board):
                            print("Checkmate! Black wins.")
                    if self.bKing.danger.visible:
                        if not self.bKing.InCheck(self.board):
                            self.bKing.danger.visible = False
        else:
            if button == mouse.LEFT:
                boardX = x // 75
                boardY = y // 75
                if self.currentPos[0] < 0 and self.currentPos[1] < 0:
                    if self.board[boardY][boardX] is not None and self.move == self.board[boardY][boardX].white:
                        self.currentPos = (boardY, boardX)
                        if self.move:
                            ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.wKing)
                        else:
                            ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.bKing)
                        if len(ValidMoves) == 0:
                            self.currentPos = (-1, -1)
                        else:
                            for move in ValidMoves:
                                self.validsprites[move[0]][move[1]].visible = True
                elif self.board[boardY][boardX] is not None and self.move == self.board[boardY][boardX].white:
                    for row in self.validsprites:
                        for sprite in row:
                            sprite.visible = False
                    self.currentPos = (boardY, boardX)
                    if self.move:
                        ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.wKing)
                    else:
                        ValidMoves = self.board[boardY][boardX].GetValidMoves(self.board, self.bKing)
                    if len(ValidMoves) == 0:
                        self.currentPos = (-1, -1)
                    else:
                        for move in ValidMoves:
                            self.validsprites[move[0]][move[1]].visible = True
                else:
                    if self.validsprites[boardY][boardX].visible:
                        self.board[boardY][boardX] = self.board[self.currentPos[0]][self.currentPos[1]]
                        self.board[self.currentPos[0]][self.currentPos[1]].ChangeLocation(boardX, boardY, self.board)
                        if type(self.board[self.currentPos[0]][self.currentPos[1]]) is Pawn and (
                                boardY == 0 or boardY == 7):
                            self.promotion = True
                            self.promoPawn = (boardY, boardX)
                        self.board[self.currentPos[0]][self.currentPos[1]] = None
                        self.currentPos = (-1, -1)
                        if self.move:
                            if self.bKing.NoValidMoves(self.board) and not self.bKing.InCheck(self.board):
                                print('Stalemate!')
                            if self.bKing.InCheck(self.board):
                                self.bKing.danger.visible = True
                                if self.bKing.NoValidMoves(self.board):
                                    print("Checkmate! White wins.")
                            if self.wKing.danger.visible:
                                if not self.wKing.InCheck(self.board):
                                    self.wKing.danger.visible = False
                            self.getLastMove()
                        else:
                            if self.wKing.NoValidMoves(self.board) and not self.wKing.InCheck(self.board):
                                print('Stalemate!')
                            if self.wKing.InCheck(self.board):
                                self.wKing.danger.visible = True
                                if self.wKing.NoValidMoves(self.board):
                                    print("Checkmate! Black wins.")
                            if self.bKing.danger.visible:
                                if not self.bKing.InCheck(self.board):
                                    self.bKing.danger.visible = False
                            self.getLastMove()
                        self.move = not self.move
                        for row in self.validsprites:
                            for sprite in row:
                                sprite.visible = False

    def update(self, dt):
        self.on_draw()
