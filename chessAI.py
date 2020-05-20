import chess

class ChessAI():
    @staticmethod
    def minimaxRoot(depth, board, isMaximizing=False):
        posMove = board.legal_moves
        bestMove = -9999
        bestMoveFinal = None
        for x in posMove:
            move = chess.Move.from_uci(str(x))

            board.push(move)
            value = max(bestMove, ChessAI.minimax(depth - 1, board, -10000, 10000, not isMaximizing))
            board.pop()
            if value > bestMove:
                print('Best score: ', str(bestMove))
                print('Best move: ', str(bestMoveFinal))
                bestMove = value
                bestMoveFinal = move

        if(bestMoveFinal==None):
            posMoves = board.legal_moves
            for x in posMoves:
                move = chess.Move.from_uci(str(x))
                bestMoveFinal = move
                break
        return str(bestMoveFinal)

    @staticmethod
    def minimax(depth, board, alpha, beta, is_maximixing):
        if depth == 0 :
            mult=-1
            if(is_maximixing):
                mult = 1
            return mult * ChessAI.evaluation(board)
        elif is_maximixing:
            posMoves = board.legal_moves
            bestMove = -9999
            for x in posMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                result = ChessAI.minimax(depth - 1, board, alpha, beta, not is_maximixing)
                bestMove = max(bestMove, result)
                print(is_maximixing,bestMove,result,alpha)
                board.pop()
                alpha = max(alpha, bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove
        else:
            posMoves = board.legal_moves
            bestMove = 9999
            for x in posMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMove = min(bestMove, ChessAI.minimax(depth - 1, board, alpha, beta, not is_maximixing))
                board.pop()
                beta = min(beta, bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove

    @staticmethod
    def evaluation(board):
        i = 0
        evaluation = 0
        x = True
        try:
            x = bool(board.piece_at(i).color)
        except AttributeError as e:
            x = x
        while i < 63:
            i += 1
            evaluation = evaluation + (
                ChessAI.getPieceValue(str(board.piece_at(i))) if x else - ChessAI.getPieceValue(str(board.piece_at(i))))
        return evaluation

    @staticmethod
    def getPieceValue(piece):
        if piece == None:
            return 0
        elif piece == "P" or piece == "p":
            return 10
        elif piece == "N" or piece == "n":
            return 30
        elif piece == "B" or piece == "b":
            return 30
        elif piece == "R" or piece == "r":
            return 50
        elif piece == "Q" or piece == "q":
            return 90
        else:
            return 900
