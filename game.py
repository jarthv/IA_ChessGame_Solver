import chess
class Game():

    def __init__(self,boardStr):
        self.board=chess.Board(boardStr+" w KQkq - 0 1")
    def doAMove(self,movestr):
        # print(movestr)
        move=chess.Move.from_uci(movestr)
        # print(move)
        if (move in self.board.legal_moves):
            isPassant = self.board.is_en_passant(move)
            castlingSide = self.getSideofCastling(move)
            self.board.push(move)
            # print(self.board)
            if(isPassant):
                return "PassantMove"
            elif(castlingSide != ""):
                return castlingSide
            return "Moved"
        else:
            return ""

    def getSideofCastling(self,move):
        result=""
        if(self.board.is_queenside_castling(move)):
            result= "queenside"
        elif(self.board.is_kingside_castling(move)):
            result= "kingside"
        return result
    def isCheckMate(self):
        return self.board.is_checkmate()
    def isCheck(self):
        return self.board.is_check()


