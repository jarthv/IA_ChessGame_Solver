import chess
import chess.polyglot
from evaluation import evaluate_board
movehistory =[]
starts = True
def negamaxRoot(depth,board,pstarts):
    global movehistory, starts
    starts = pstarts == "w"
    bestMove = chess.Move.null()
    bestValue = -99999
    alpha = -100000
    beta = 100000
    greaterProximity = 0
    possibleMoves = board.legal_moves
    for move in possibleMoves:

        board.push(move)
        result =alphabeta(-beta, -alpha, depth-1,board)
        score = - result[0]
        if(score == bestValue and result[1]>greaterProximity):
            bestMove= move
            greaterProximity=result[1]

        if score > bestValue:
            bestValue = score
            bestMove = move
            greaterProximity=result[1]
        score = max(score,alpha)
        board.pop()
    return bestMove



def alphabeta( alpha, beta, depthleft,board ):
    bestscore = -9999
    greaterProximity=0
    if( depthleft == 0 ):
        return (quiesce( alpha, beta ,board),0)
    if(board.is_stalemate() or board.is_checkmate()):
        return (evaluate_board(board), depthleft)
    possibleMoves = board.legal_moves
    for move in possibleMoves:
        board.push(move)
        result = alphabeta( -beta, -alpha, depthleft - 1,board )
        score = -result[0]
        board.pop()
        if( score >= beta ):
            return (score,result[1])
        bestscore = max(bestscore,score,)
        if(score == bestscore and result[1]>greaterProximity):
            greaterProximity=result[1]
        alpha = max(score,alpha)
    return (bestscore,greaterProximity)

def quiesce( alpha, beta ,board):
    stand_pat = evaluate_board(board)
    if( stand_pat >= beta ):
        return beta
    if( alpha < stand_pat ):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce( -beta, -alpha,board )
            board.pop()

            if( score >= beta ):
                return beta
            if( score > alpha ):
                alpha = score
    return alpha
