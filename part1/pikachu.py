#
# pikachu.py : Play the game of Pikachu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, March 2021
#
import itertools
import sys
import time
import numpy as np
import copy


def Minimax(CurrentState, level, player, visitedstates, recursiondepth):
    if recursiondepth == 3:
        return EvaluateState(CurrentState, player), CurrentState
    if player == 'w' and len(CurrentState.w_pieces) == 0:
        visitedstates.append((-10*EvaluateState(CurrentState, player), CurrentState))
        return -10*EvaluateState(CurrentState, player), CurrentState
    elif player == 'w' and len(CurrentState.b_pieces) == 0:
        visitedstates.append((10*EvaluateState(CurrentState, player), CurrentState))
        return 10*EvaluateState(CurrentState, player), CurrentState
    elif player == 'b' and len(CurrentState.b_pieces) == 0:
        visitedstates.append((-10*EvaluateState(CurrentState, player), CurrentState))
        return -10*EvaluateState(CurrentState, player), CurrentState
    elif player == 'b' and len(CurrentState.b_pieces) == 0:
        visitedstates.append((10*EvaluateState(CurrentState, player), CurrentState))
        return 10*EvaluateState(CurrentState, player), CurrentState

    if level == 'Min':
        for item in visitedstates:
            if CurrentState == item[1]:
                return item[0], item[1]
        next_States = CurrentState.GetNextMoves('b' if player=='w' else 'w')
        min_value = None
        for state in next_States:
            bestnode_State = Minimax(state, 'Max', 'b' if player == 'w' else 'w', visitedstates, recursiondepth + 1)
            if min_value is None:
                min_value = bestnode_State[0], state
            else:
                min_value = min([min_value, (bestnode_State[0], state)], key=lambda t: t[0])
        return min_value[0], min_value[1]

    elif level == 'Max':
        for item in visitedstates:
            if CurrentState == item[1]:
                return item[0], item[1]
        next_States = CurrentState.GetNextMoves(player)
        max_value = None
        for state in next_States:
            bestnode_State = Minimax(state, 'Min', player, visitedstates, recursiondepth + 1)
            if max_value is None:
                max_value = bestnode_State[0], state
            else:
                max_value = max([max_value, (bestnode_State[0], state)], key=lambda t:t[0])
        return max_value[0],max_value[1]


def EvaluateState(State, player):
    if player == 'w':
        return -len(State.b_pieces)
    return -len(State.w_pieces)


class Move:
    def __init__(self, previous, current, captures):
        '''

        :param previous: the previous index of piece which has moved
        :param current: current index of piece which has moved
        :param captures: index of piece which got captured
        '''
        self.previous = previous
        self.current = current
        self.captures = captures


def UpdateBoard(State, move, player):
    '''
    :param board: current state of the board
    :param move: the move with which to update the board
    :return: sends a new board with updated state. Also calls remove piece function which marks a captured piece,
     if piece was captured on the move
    '''
    if player.color == 'w':
        opposite = State.b_pieces
        own = State.w_pieces
    else:
        opposite = State.w_pieces
        own = State.b_pieces
    if len(move.captures) != 0:
        captured = None
        for p in opposite:
            if p.position == move.captures:
                captured = p
                break
        if captured.color == 'w':
            State.w_pieces.remove(captured)
            State.board[move.captures[0]][move.captures[1]] = '.'
        else:
            State.b_pieces.remove(captured)
            State.board[move.captures[0]][move.captures[1]] = '.'
    moved = None
    for p in own:
        if p.position == move.previous:
            p.position = move.current
            moved = p
            break
    State.board[move.previous[0]][move.previous[1]] = '.'
    State.board[move.current[0]][move.current[1]] = moved.character
    if player.color == 'w' and move.current[0] == len(State.board)-1:
        State.PromotePiece(move.current, player)
        State.board[move.current[0]][move.current[1]] = 'W'
    if player.color == 'b' and move.current[0] == 0:
        State.PromotePiece(move.current, player)
        State.board[move.current[0]][move.current[1]] = 'B'
    return State


class State:
    '''
    board - the board configuration in current state
    w_pieces - the list of white pieces and their positions
    b_pieces - the list of black pieces and their positions
    '''
    def __init__(self, board, w_pieces, b_pieces):
        self.board = board
        self.w_pieces = w_pieces
        self.b_pieces = b_pieces

    def GetNextMoves(self, player):
        NextStates = []
        if player == 'w':
            for p in self.w_pieces:
                for move in p.findvalidmoves(copy.deepcopy(self.board)):
                    NextStates.append(UpdateBoard(copy.deepcopy(self), move,p))

        else:
            for p in self.b_pieces:
                for move in p.findvalidmoves(copy.deepcopy(self.board)):
                    NextStates.append(UpdateBoard(copy.deepcopy(self), move, p))
        return NextStates

    def PromotePiece(self, position, player):
        if player.color == 'w':
            promoted = None
            for p in self.w_pieces:
                if p.position==position:
                    promoted = p
                    break
            self.w_pieces.remove(p)
            new_piece = Pikachu('w', p.position, 'W')
            self.w_pieces.append(new_piece)
        else:
            if player.color == 'b':
                promoted = None
                for p in self.b_pieces:
                    if p.position == position:
                        promoted = p
                        break
                self.b_pieces.remove(p)
                new_piece = Pikachu('b', p.position, 'B')
                self.b_pieces.append(new_piece)


class pichu:
    def __init__(self, color, position, character):
        self.color = color
        self.captured = False
        self.position = position
        self.character = character

    def findvalidmoves(self, b):
        validmoves = ['left', 'right']
        if self.color == 'w':
            validmoves.append('forward')
        else:
            validmoves.append('back')
        if self.position[0] == len(b)-1:
            if 'forward' in validmoves:
                validmoves.remove('forward')
        if self.position[0] == 0:
            if 'back' in validmoves:
                validmoves.remove('back')
        if self.position[1] == len(b[0])-1:
            validmoves.remove('right')
        if self.position[1] == 0:
            validmoves.remove('left')
        return self.GetValidPositions(validmoves, b)

    def GetValidPositions(self, validmoves, b):
        validpositions = []
        if self.color == 'w':
            for move in validmoves:
                if move == 'forward' and b[self.position[0] + 1][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] + 1, self.position[1]], []))
                if move == 'forward' and self.position[0] + 2 < len(b) and (b[self.position[0] + 1][
                                                                                self.position[1]] == 'b' or
                                                                            self.position[0] + 2 < len(b) and
                                                                            b[self.position[0] + 1][
                                                                                self.position[1]] == 'B') \
                        and b[self.position[0] + 2][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] + 2, self.position[1]],
                                               [self.position[0] + 1, self.position[1]]))
                if move == 'left' and b[self.position[0]][self.position[1] - 1] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] - 1], []))
                if move == 'left' and self.position[1] - 2 >= 0 and (b[self.position[0]][self.position[1] - 1] == 'b' or
                                                                     b[self.position[0]][self.position[1] - 1] == 'B') \
                        and b[self.position[0]][self.position[1] - 2] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] - 2],
                                               [self.position[0], self.position[1] - 1]))
                if move == 'right' and b[self.position[0]][self.position[1] + 1] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] + 1], []))
                if move == 'right' and self.position[1] + 2 < len(b[0]) and (b[self.position[0]][
                                                                                 self.position[1] + 1] == 'b' or
                                                                             b[self.position[0]][
                                                                                 self.position[1] + 1] == 'B') \
                        and b[self.position[0]][self.position[1] + 2] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] + 2],
                                               [self.position[0], self.position[1] + 1]))
                if move == 'back' and b[self.position[0] - 1][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] - 1, self.position[1]], []))
                if move == 'back' and self.position[0] - 2 >= 0 and (b[self.position[0] - 1][
                                                                         self.position[1]] == 'b' or
                                                                     b[self.position[0] - 1][self.position[1]] == 'B') \
                        and b[self.position[0] - 2][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] - 2, self.position[1]],
                                               [self.position[0] - 1, self.position[1]]))
        else:
            for move in validmoves:
                if move == 'forward' and b[self.position[0] + 1][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] + 1, self.position[1]], []))
                if move == 'forward' and self.position[0] + 2 < len(b) and (b[self.position[0] + 1][
                                                                                self.position[1]] == 'w' or
                                                                            b[self.position[0] + 1][
                                                                                self.position[1]] == 'W') \
                        and b[self.position[0] + 2][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] + 2, self.position[1]],
                                               [self.position[0] + 1, self.position[1]]))
                if move == 'left' and b[self.position[0]][self.position[1] - 1] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] - 1], []))
                if move == 'left' and self.position[1] - 2 >= 0 and (b[self.position[0]][self.position[1] - 1] ==
                                                                     'w' or b[self.position[0]][
                                                                         self.position[1] - 1] == 'W') \
                        and b[self.position[0] - 2][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] - 2],
                                               [self.position[0], self.position[1] - 1]))
                if move == 'right' and b[self.position[0]][self.position[1] + 1] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] + 1], []))
                if move == 'right' and self.position[1] + 2 < len(b[0]) and (b[self.position[0]][
                                                                                 self.position[1] + 1] == 'w' or
                                                                             b[self.position[0]][
                                                                                 self.position[1] + 1] == 'W') \
                        and b[self.position[0]][self.position[1] + 2] == '.':
                    validpositions.append(Move(self.position, [self.position[0], self.position[1] + 2],
                                               [self.position[0], self.position[1] + 1]))
                if move == 'back' and b[self.position[0] - 1][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] - 1, self.position[1]], []))
                if move == 'back' and self.position[0] - 2 >= 0 and (b[self.position[0] - 1][self.position[1]] ==
                                                                     'w' or b[self.position[0] - 1][
                                                                         self.position[1]] == 'W') \
                        and b[self.position[0] - 2][self.position[1]] == '.':
                    validpositions.append(Move(self.position, [self.position[0] - 2, self.position[1]],
                                               [self.position[0] - 1, self.position[1]]))
        return validpositions


class Pikachu:
    def __init__(self, color, position, character):
        self.color = color
        self.captured = False
        self.position = position
        self.character = character

    def findvalidmoves(self, b):
        validmoves = ['left', 'right', 'forward', 'back']
        if self.position[0] == len(b) - 1:
            if 'forward' in validmoves:
                validmoves.remove('forward')
        if self.position[0] == 0:
            if 'back' in validmoves:
                validmoves.remove('back')
        if self.position[1] == len(b[0]) - 1:
            validmoves.remove('right')
        if self.position[1] == 0:
            validmoves.remove('left')
        return self.GetValidPositions(validmoves, b)

    def GetValidPositions(self, validmoves, b):
        validMoves = []
        if 'forward' in validmoves:
            validMoves.extend([move for move in self.WalkForward(self.position, b)])
        if 'back' in validmoves:
            validMoves.extend([move for move in self.WalkBack(self.position, b)])
        if 'right' in validmoves:
            validMoves.extend([move for move in self.WalkRight(self.position, b)])
        if 'left' in validmoves:
            validMoves.extend([move for move in self.WalkLeft(self.position, b)])

        return validMoves

    def WalkForward(self, position, b):
        moves = []
        jumpedpiece = []
        jumped = 0
        current = position[0]
        while current + 1 <= len(b) - 1 and b[current + 1][position[1]] == '.':
            moves.append(Move(self.position, [current + 1, position[1]], []))
            current += 1
        if current +1 <= len(b) - 1:
            if self.color == 'w' and (b[current+1][position[1]] == 'b' or b[current+1][position[1]] == 'B'):

                jumpedpiece = [current+1,position[1]]
                current += 2
                jumped = 1
            elif self.color == 'b' and (b[current+1][position[1]] == 'w' or b[current+1][position[1]] == 'W'):

                jumpedpiece = [current+1,position[1]]
                current += 2
                jumped = 1
        if jumped:
            if self.color == 'w':
                while current <= len(b) - 1 and (b[current][position[1]] != 'b' or b[current][position[1]] != 'B') and b[current][position[1]] == '.':
                    moves.append(Move(self.position, [current, position[1]], jumpedpiece))
                    current += 1
            if self.color == 'b':
                while current <= len(b) - 1 and (b[current][position[1]] != 'w' or b[current+1][position[1]] != 'W') and b[current][position[1]] == '.':
                    moves.append(Move(self.position, [current, position[1]], jumpedpiece))
                    current += 1
        return moves


    def WalkRight(self, position, b):
        moves = []
        jumpedpiece = []
        jumped = 0
        current = position[1]
        while current + 1 <= len(b[0])-1 and b[position[0]][current + 1] == '.':
            moves.append(Move(self.position, [position[0], current + 1], []))
            current += 1
        if current + 1 <= len(b[0])-1:
            if self.color == 'w' and (b[position[0]][current + 1] == 'b' or b[position[0]][current + 1] == 'B'):
                jumpedpiece = [position[0], current + 1]
                current += 2
                jumped = 1
        if current + 1 <= len(b[0])-1:
            if self.color == 'b' and (b[position[0]][current + 1] == 'w' or b[position[0]][current + 1] == 'W'):
                jumpedpiece = [position[0],current + 1]
                current += 2
                jumped = 1
        if jumped:
            if self.color == 'w':
                while current <= len(b[0]) - 1 and (b[position[0]][current] != 'b' or b[position[0]][current] != 'B') and \
                        b[position[0]][current] == '.':
                    moves.append(Move(self.position, [position[0], current], jumpedpiece))
                    current += 1
            if self.color == 'b':
                while current <= len(b) - 1 and (b[position[0]][current] != 'w' or b[position[0]][current] != 'W') \
                        and b[position[0]][current] == '.':
                    moves.append(Move(self.position, [position[0],current], jumpedpiece))
                    current += 1
        return moves


    def WalkLeft(self, position, b):
        moves = []
        jumpedpiece = []
        jumped = 0
        current = position[1]
        while current - 1 >= 0 and b[position[0]][current - 1] == '.':
            moves.append(Move(self.position, [position[0], current - 1], []))
            current -= 1
        if current - 1 >= 0:
            if self.color == 'w' and (b[position[0]][current - 1] == 'b' or b[position[0]][current - 1] == 'B'):
                jumpedpiece = [position[0], current - 1]
                current -= 2
                jumped = 1
            elif self.color == 'b' and (b[position[0]][current - 1] == 'w' or b[position[0]][current - 1] == 'W'):
                jumpedpiece = [position[0], current - 1]
                current -= 2
                jumped = 1
        if jumped:
            if self.color == 'w':
                while current >= 0 and (b[position[0]][current] != 'b' or b[position[0]][current] != 'B') and \
                        b[position[0]][current] == '.':
                    moves.append(Move(self.position, [position[0], current], jumpedpiece))
                    current -= 1
            if self.color == 'b':
                while current >= 0 and (b[position[0]][current] != 'w' or b[position[0]][current] != 'W') \
                        and b[position[0]][current] == '.':
                    moves.append(Move(self.position, [position[0], current], jumpedpiece))
                    current -= 1
        return moves


    def WalkBack(self, position, b):
        moves = []
        jumpedpiece = []
        jumped = 0
        current = position[0]
        while current - 1 >= 0 and b[current - 1][position[1]] == '.':
            moves.append(Move(self.position, [current - 1, position[1]], []))
            current -= 1
        if current - 1 >= 0:
            if self.color == 'w' and (b[current - 1][position[1]] == 'b' or b[current - 1][position[1]] == 'B'):
                jumpedpiece = [current - 1, position[1]]
                current -= 2
                jumped = 1
            if self.color == 'b' and (b[current - 1][position[1]] == 'w' or b[current - 1][position[1]] == 'W'):
                jumpedpiece = [current - 1, position[1]]
                current -= 2
                jumped = 1
        if jumped:
            if self.color == 'w':
                while current >= 0 and (b[current][position[1]] != 'b' or b[current][position[1]] != 'B') and \
                        b[current][position[1]] == '.':
                    moves.append(Move(self.position, [current, position[1]], jumpedpiece))
                    current -= 1
            if self.color == 'b':
                while current >= 0 and (
                        b[current][position[1]] != 'w' or b[current + 1][position[1]] != 'W') and b[current][position[1]] == '.':
                    moves.append(Move(self.position, [current, position[1]], jumpedpiece))
                    current -= 1
        return moves


def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


def GetPieces(board, N):
    w_pieces = []
    b_pieces = []
    for i in range(N):
        for j in range(N):
            if board[i][j]!='.':

                if board[i][j] == 'w':
                    w_pieces.append(pichu('w', [i, j],'w'))
                elif board[i][j] == 'W':
                    w_pieces.append(Pikachu('w', [i, j],'W'))
                elif board[i][j] == 'b':
                    b_pieces.append(pichu('b', [i, j],'b'))
                else:
                    b_pieces.append(Pikachu('b', [i, j], 'B'))
    return w_pieces, b_pieces


def ConvertBoardTo2d(board, N):
    board_2d = [['.' for _ in range(N)] for _ in range(N)]
    count = 0
    for i in range(N):
        for j in range(N):
            board_2d[i][j] = board[count]
            count += 1
    return board_2d


def ConvertBoardTo1d(board, N):
    board1d =[]
    for i in range(N):
        board1d.extend(board[i])
    return board1d


def GenerateValidMoves(w_pieces, b_pieces, board_2d, player):
    valid_moves = []
    if player=='w':
        for piece in w_pieces:

            if piece.position[0]+1 < N and board_2d[piece.position[0]+1][piece.position[1]] == '.':
                board = copy.deepcopy(board_2d)
                board[piece.position[0]][piece.position[1]] = '.'
                board[piece.position[0] + 1][piece.position[1]] = 'w'
                valid_moves.append(copy.deepcopy(board))
                del board
            if piece.position[1]-1 >= 0 and board_2d[piece.position[0]][piece.position[1]-1] == '.':
                board = copy.deepcopy(board_2d)
                board[piece.position[0]][piece.position[1]] = '.'
                board[piece.position[0] + 1][piece.position[1]] = 'w'
                valid_moves.append(copy.deepcopy(board))
                del board
            if piece.position[1]+1 < N and board_2d[piece.position[0]][piece.position[1]+1] == '.':
                board = copy.deepcopy(board_2d)
                board[piece.position[0]][piece.position[1]] = '.'
                board[piece.position[0]][piece.position[1]+1] = 'w'
                valid_moves.append(copy.deepcopy(board))
                del board
            if piece.position[0]+2 < N and board_2d[piece.position[0]+1][piece.position[1]] == ('b' or 'B'):
                if board_2d[piece.position[0]+2][piece.position[1]]=='.':
                    board = copy.deepcopy(board_2d)
                    board[piece.position[0]][piece.position[1]] = '.'
                    board[piece.position[0]+1][piece.position[1]] = '.'
                    board[piece.position[0] + 2][piece.position[1]] = 'w'
                    valid_moves.append(copy.deepcopy(board))
                    del board
            if piece.position[1]-2 < N and board_2d[piece.position[0]][piece.position[1]-1] == ('b' or 'B'):
                if board_2d[piece.position[0]][piece.position[1]-2]=='.':
                    board = copy.deepcopy(board_2d)
                    board[piece.position[0]][piece.position[1]-1] = '.'
                    board[piece.position[0]][piece.position[1]] = '.'
                    board[piece.position[0]][piece.position[1]-2] = 'w'
                    valid_moves.append(copy.deepcopy(board))
                    del board
            if piece.position[1] + 2 < N and board_2d[piece.position[0]][piece.position[1] + 1] == ('b' or 'B'):
                if board_2d[piece.position[0]][piece.position[1] + 2] == '.':
                    board = copy.deepcopy(board_2d)
                    board[piece.position[0]][piece.position[1] + 1] = '.'
                    board[piece.position[0]][piece.position[1]] = '.'
                    board[piece.position[0]][piece.position[1]+2] = 'w'
                    valid_moves.append(copy.deepcopy(board))
                    del board

    return valid_moves


def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    board_2d = ConvertBoardTo2d(board,N)
    w_pieces, b_pieces = GetPieces(board_2d, N)
    current_state = State(board_2d, w_pieces, b_pieces)
    visited_states = []
    recursiondepth = 0
    best_move = Minimax(current_state, 'Max', player, visited_states, recursiondepth)
    while True:
        # # start = time.time()
        # boards = current_state.GetNextMoves(player)
        # # print(time.time() - start)
        # # current_state = boards[0]
        #
        # if player =='w':
        #     boards = sorted(boards,key=lambda t:EvaluateState(t, player))
        # else:
        #     boards = sorted(boards, key=lambda t:EvaluateState(t, player))
        board_string = ConvertBoardTo1d(best_move[1].board, N)
        board_string = "".join(str(i) for i in board_string)
        # yield board_to_string(board_string, N)
        yield board_string


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: pikachu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
