import chess
from chessAI import minimaxRoot
class Game():

    def __init__(self,boardStr):
        self.board=chess.Board(boardStr)
    def doAMove(self,movestr):
        # print(movestr)
        move=chess.Move.from_uci(movestr)

        if (move in self.board.legal_moves):
            isPassant = self.board.is_en_passant(move)
            castlingSide = self.getSideofCastling(move)
            sanMove=str(self.board.san(move))
            self.board.push(move)

            # print(self.board)
            if(isPassant):
                return ("PassantMove",sanMove)
            elif(castlingSide != ""):
                return (castlingSide,sanMove)
            return ("Moved",sanMove)
        else:
            return ("","")

    def getSideofCastling(self,move):
        result=""
        if(self.board.is_queenside_castling(move)):
            result= "queenside"
        elif(self.board.is_kingside_castling(move)):
            result= "kingside"
        return result
    def isCheckMate(self):
        return self.board.is_checkmate()
    def isStalemate(self):
        return self.board.is_stalemate()
    def isCheck(self):
        return self.board.is_check()

    def suggestedMove(self,turn):
        t= False
        if(turn=="B"):
            t = True
        return minimaxRoot(2, self.board,t)
    def isvalid(self):
        return self.board.is_valid() or self.isStalemate() or self.isCheckMate()



