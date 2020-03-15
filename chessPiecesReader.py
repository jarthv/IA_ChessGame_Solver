
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.king import *
from pieces.pawn import Pawn


class ChessPiecesReader(object):
    __colPositions = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    def __init__(self):
        pass

    def __standartBoard(self):
        wKing = King(4, 0)
        bKing = King(4, 7, False)
        result = [[[Rook(0, 0), Knight(1, 0), Bishop(2, 0), Queen(3, 0), wKing, Bishop(5, 0),
                  Knight(6, 0), Rook(7, 0)],
                 [Pawn(i, 1) for i in range(8)],
                 [None for i in range(8)],
                 [None for i in range(8)],
                 [None for i in range(8)],
                 [None for i in range(8)],
                 [Pawn(i, 6, False) for i in range(8)],
                 [Rook(0, 7, False), Knight(1, 7, False), Bishop(2, 7, False), Queen(3, 7, False),
                  bKing, Bishop(5, 7, False), Knight(6, 7, False), Rook(7, 7, False)]], wKing, bKing]
        return result

    def __pieceGenerator(self,type, piece,x,y):
        if piece == "R":
            return King(x, y,type)
        elif piece == "Q":
            return Queen(x, y,type)
        elif piece == "T":
            return Rook(x, y, type)
        elif piece == "C":
            return Knight(x, y, type)
        elif piece == "A":
            return Bishop(x, y, type)
        elif piece == "P":
            return Pawn(x, y, type)

    def __colourToType(self,colour):
        if colour == "B":
            return True
        return False

    def __formatToBoard(self,textPositions=[]):
        wKing = None
        bKing = None
        board =[[None for i in range(8)] for i in range (8)]

        if not textPositions:
            return self.__standartBoard()
        else:
            for i in textPositions:
                x= self.__colPositions[i[2]]
                y=int(i[3]) - 1
                p = self.__pieceGenerator(self.__colourToType(i[0]),i[1],x,y)
                if i[1] == "R":
                    if i[0] == "B":
                        wKing = p
                    else:
                        bKing = p
                board[y][x] = p
                print(board)

            return [board, wKing, bKing]

    def readFile(self,filename=""):
        game1 = ["BTf1", "NTe7", "BAd5", "BRd6", "NRd8"]
        return self.__formatToBoard(game1)





