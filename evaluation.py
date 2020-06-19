import chess

starts = False
def evaluate_board(board):
    global starts
    if board.is_checkmate():
        if board.turn == starts or not board.turn == starts:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    eval = evaluateMaterial(board,True)-evaluateMaterial(board,False)+ evaluatePosition(board,True)-evaluatePosition(board,False)+connectionValue(board,True) - connectionValue(board,False)
    if board.turn == starts or not board.turn == starts:
        return eval
    else:
        return -eval


value = {"P":100,"N":320,"B":330,"R":500,"Q":900}

def evaluateMaterial(board,turn):
    p = value["P"] * len(board.pieces(chess.PAWN, turn))
    n = value["N"] * len(board.pieces(chess.KNIGHT, turn))
    b = value["B"] * len(board.pieces(chess.BISHOP, turn))
    r = value["R"] * len(board.pieces(chess.ROOK, turn))
    q = value["Q"] * len(board.pieces(chess.QUEEN, turn))
    return  p+n+b+r+q



def connectionValue(board,turn):
    dv=defendedValue(board,turn)
    av= attackedValue(board,turn)
    result = dv-av
    if(dv<av):
        result -= ((av-dv)*10)
    return result

def defendedValue(board,turn):
    pieces=set()
    map =board.piece_map()
    keys = map.keys()
    for x in keys:
        if (board.color_at(x)==turn):
            for e in board.attackers(turn,x):
                if (x not in board.pieces(chess.KING, turn)):
                    pieces.add(x)
    return len(pieces)*10

def attackedValue(board,pturn):
    turn = not pturn
    pieces=set()
    map =board.piece_map()
    keys = map.keys()
    for x in keys:
        if (board.color_at(x)== (not turn)):
            for e in board.attackers(turn,x):
                if (x not in board.pieces(chess.KING, turn)):
                    pieces.add(x)
    return len(pieces) * 10


def main():
    board = chess.Board("rnb1k2r/ppp2ppp/5n2/3q4/1b1P4/2N5/PP3PPP/R1BQKBNR w KQkq - 3 7")
    defendedValue(board,True)
    attackedValue(board,True)
if __name__ == '__main__':
    main()

def mirrorSquare(turn,piece):
    if(turn):
        return piece
    return chess.square_mirror(piece)


def evaluatePosition(board,turn):
    pawnsq = sum([pawntable[mirrorSquare(turn,i)] for i in board.pieces(chess.PAWN, turn)])
    knightsq = sum([knightstable[mirrorSquare(turn,i)] for i in board.pieces(chess.KNIGHT, turn)])
    bishopsq= sum([bishopstable[mirrorSquare(turn,i)] for i in board.pieces(chess.BISHOP, turn)])
    rooksq = sum([rookstable[mirrorSquare(turn,i)] for i in board.pieces(chess.ROOK, turn)])
    queensq = sum([queenstable[mirrorSquare(turn,i)] for i in board.pieces(chess.QUEEN, turn)])
    kingsq = sum([kingstableFinal[mirrorSquare(turn,i)] for i in board.pieces(chess.KING, turn)])

    return pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq

pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]


kingstableFinal = [
-50,-30,-30,-30,-30,-30,-30,-50,
-30, -30, 0, 0, 0, 0, -30, -30,
-30, -10, 20, 30, 30, 20, -10, -30,
-30, -10, 30, 40, 40, 30, -10, -30,
-30, -10, 30, 40, 40, 30, -10, -30,
-30, -10, 20, 30, 30, 20, -10, -30,
-30, -20, -10, 0, 0, -10, -20, -30,
-50,-40,-30,-20,-20,-30,-40,-50]
