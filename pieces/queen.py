from .piece import *

class Queen(Piece):
    def __init__(self, x, y, type=True):
        super(Queen, self).__init__(type)
        if self.white:
            self.pieceimage = spritesheet[WHITE_QUEEN]
        else:
            self.pieceimage = spritesheet[BLACK_QUEEN]
        self.piecesprite = pyglet.sprite.Sprite(self.pieceimage, x * 75, y * 75)

    def GetThreatSquares(self, board):
        x = int(self.piecesprite.x // 75)
        y = int(self.piecesprite.y // 75)
        ListOfMoves = []
        if y > 0:
            for i in range(y - 1, -1, -1):
                if board[i][x] is not None:
                    if board[i][x].white != self.white:
                        ListOfMoves.append((i, x))
                    break
                ListOfMoves.append((i, x))
        if y < 7:
            for i in range(y + 1, 8):
                if board[i][x] is not None:
                    if board[i][x].white != self.white:
                        ListOfMoves.append((i, x))
                    break
                ListOfMoves.append((i, x))
        if x > 0:
            for i in range(x - 1, -1, -1):
                if board[y][i] is not None:
                    if board[y][i].white != self.white:
                        ListOfMoves.append((y, i))
                    break
                ListOfMoves.append((y, i))
        if x < 7:
            for i in range(x + 1, 8):
                if board[y][i] is not None:
                    if board[y][i].white != self.white:
                        ListOfMoves.append((y, i))
                    break
                ListOfMoves.append((y, i))
        for i in range(1, 8):
            if y-i < 0 or x-i < 0:
                break
            if board[y-i][x-i] is not None:
                if board[y-i][x-i].white != self.white:
                    ListOfMoves.append((y-i, x-i))
                break
            ListOfMoves.append((y-i, x-i))
        for i in range(1, 8):
            try:
                if board[y+i][x+i] is not None:
                    if board[y+i][x+i].white != self.white:
                        ListOfMoves.append((y+i, x+i))
                    break
                ListOfMoves.append((y+i, x+i))
            except IndexError:
                break
        for i in range(1, 8):
            try:
                if x-i < 0:
                    break
                if board[y+i][x-i] is not None:
                    if board[y+i][x-i].white != self.white:
                        ListOfMoves.append((y+i, x-i))
                    break
                ListOfMoves.append((y+i, x-i))
            except IndexError:
                break
        for i in range(1, 8):
            try:
                if y - i < 0:
                    break
                if board[y-i][x+i] is not None:
                    if board[y-i][x+i].white != self.white:
                        ListOfMoves.append((y-i, x+i))
                    break
                ListOfMoves.append((y-i, x+i))
            except IndexError:
                break
        return ListOfMoves
