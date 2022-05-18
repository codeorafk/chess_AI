import board, pieces, numpy

class Heuristics:

    # The tables denote the points scored for the position of the chess pieces on the board.

    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    KING_TABLE = numpy.array([
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [ 20,  20,   0,   0,   0,   0,  20,  20],
        [ 20,  30,  10,   0,   0,  10,  30,  20]
    ])
    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)

        position = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if piece != 0:
                    if piece.piece_type == pieces.Pawn.PIECE_TYPE:
                        table = Heuristics.PAWN_TABLE
                    if piece.piece_type == pieces.Knight.PIECE_TYPE:
                        table = Heuristics.KNIGHT_TABLE
                    if piece.piece_type == pieces.Bishop.PIECE_TYPE:
                        table = Heuristics.BISHOP_TABLE
                    if piece.piece_type == pieces.Rook.PIECE_TYPE:
                        table = Heuristics.ROOK_TABLE
                    if piece.piece_type == pieces.Queen.PIECE_TYPE:
                        table = Heuristics.QUEEN_TABLE
                    if piece.piece_type == pieces.King.PIECE_TYPE:
                        table = Heuristics.KING_TABLE
                    position += Heuristics.get_piece_position_score(piece, table, x, y)
        return material + position

    # Returns the score for the position of the given type of piece.
    # A piece type can for example be: pieces.Pawn.PIECE_TYPE.
    # The table is the 2d numpy array used for the scoring. Example: Heuristics.PAWN_TABLE
    @staticmethod
    def get_piece_position_score(piece, table, x, y):
        if (piece.color == pieces.Piece.WHITE):
            return table[x][y]
        else:
            return -(table[7 - x][y])

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == pieces.Piece.WHITE):
                        white += piece.value
                    else:
                        black += piece.value

        return white - black


class AI:

    INFINITE = 10000000

    @staticmethod
    def get_ai_move(chessboard, invalid_moves, depth):
        best_move = 0
        best_score = AI.INFINITE
        for move in chessboard.get_possible_moves(pieces.Piece.BLACK):
            if (AI.is_invalid_move(move, invalid_moves)):
                continue

            copy = board.Board.clone(chessboard)
            copy.perform_move(move)

            score = AI.alphabeta(copy, depth, -AI.INFINITE, AI.INFINITE, True)
            if (score < best_score):
                best_score = score
                best_move = move

        # Checkmate.
        if (best_move == 0):
            return 0

        copy = board.Board.clone(chessboard)
        copy.perform_move(best_move)
        if (copy.is_check(pieces.Piece.BLACK)):
            invalid_moves.append(best_move)
            return AI.get_ai_move(chessboard, invalid_moves, depth)

        return best_move

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if (invalid_move.equals(move)):
                return True
        return False

    @staticmethod
    def minimax(board, depth, maximizing):
        if (depth == 0):
            return Heuristics.evaluate(board)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in board.get_possible_moves(pieces.Piece.WHITE):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in board.get_possible_moves(pieces.Piece.BLACK):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, True)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(chessboard, depth, a, b, maximizing):
        if (depth == 0):
            return Heuristics.evaluate(chessboard)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in chessboard.get_possible_moves(pieces.Piece.WHITE):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False))
                a = max(a, best_score)
                if (b <= a):
                    break
            return best_score
        else:
            best_score = AI.INFINITE
            for move in chessboard.get_possible_moves(pieces.Piece.BLACK):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True))
                b = min(b, best_score)
                if (b <= a):
                    break
            return best_score


class Move:

    def __init__(self, xfrom, yfrom, xto, yto, castling_move):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto
        self.castling_move = castling_move

    # Returns true iff (xfrom,yfrom) and (xto,yto) are the same.
    def equals(self, other_move):
        return self.xfrom == other_move.xfrom and self.yfrom == other_move.yfrom and self.xto == other_move.xto and self.yto == other_move.yto

    def to_string(self):
        return "(" + str(self.xfrom) + ", " + str(self.yfrom) + ") -> (" + str(self.xto) + ", " + str(self.yto) + ")"
