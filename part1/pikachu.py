#
# pikachu.py : Play the game of Pikachu
# shmoham@iu.edu
# spanampi@iu.edu
# vsiyer@iu.edu
#
# Based on skeleton code by D. Crandall, March 2021
#
import itertools
import sys
import time
import numpy as np
import copy
import math

def Minimax(CurrentState, level, player, visitedstates, recursiondepth, alpha, beta):
    '''
    :param CurrentState: The current state of the game - 1. the board as a 2d list with characters in positions after
    moves in the game 2. the list of white's and black's pieces represented by pichu or Pikachu class Objects - objects contain
      attributes position ,color, character
      like
    :param level: whether the intended call is for min or max
    :param player: whether the player is min or max  - in our case if original player was w, then on call to min, the player
     is b, then w for max alternatively
    :param visitedstates: in case of repeated moves, we will store a the state and its value in a list, and return this
    value as soon as the same state is encountered
    :param recursiondepth: value to keep track of which level we are in the game tree, at certain level, we will directly return
    a value of the board state, computed using the evaluation function, instead of looking for the terminal state, which is either player having all
     pieces captured
    :return: a tuple consisting 1. a value which is output by the evaluation function after looking at the board State and
    attributes of the pieces such that chances of winning the game are maximized 2. a State object which is the calling function for that evaluation - if leaf node/ max depth level,
     then returned value is evaluation of the leaf node, max code block returns a tuple with 1st element having maximum value and 2nd element is the calling state, similarly min returns 1st element haing min state
      and its calling state
    '''
    if recursiondepth == 3:
        return EvaluateState(CurrentState, player), alpha, beta
    # append to visited state to reuse later, since this State subtree has been computed
    if player == 'w' and len(CurrentState.w_pieces) == 0:
        visitedstates.append((-10*EvaluateState(CurrentState, player), CurrentState))
        return -10*EvaluateState(CurrentState, player), alpha, beta
    elif player == 'w' and len(CurrentState.b_pieces) == 0:
        visitedstates.append((10*EvaluateState(CurrentState, player), CurrentState))
        return 10*EvaluateState(CurrentState, player), alpha, beta
    elif player == 'b' and len(CurrentState.b_pieces) == 0:
        visitedstates.append((-10*EvaluateState(CurrentState, player), CurrentState))
        return -10*EvaluateState(CurrentState, player), alpha, beta
    elif player == 'b' and len(CurrentState.w_pieces) == 0:
        visitedstates.append((10*EvaluateState(CurrentState, player), CurrentState))
        return 10*EvaluateState(CurrentState, player), alpha, beta
        ''' Min code block - checks if the state passed to it is already checked, otherwise checks the next states of passed
        state and returns the min value of those states.
        '''
    if level == 'Min':
        for item in visitedstates:
            if CurrentState == item[1]:
                return item[0], alpha, beta
        # Get all the next states of the passed state, then compute the min of those
        # states by passing each of them in turn to minimax
        # function
        next_States = CurrentState.GetNextMoves('b' if player=='w' else 'w')
        min_value = math.inf

        for state in next_States:
            bestnode_State, alpha, beta = Minimax(state, 'Max', player, visitedstates, recursiondepth+1, alpha,beta)
            min_value = min([min_value, bestnode_State])
            if min_value < alpha:
                return min_value, alpha, beta
            beta = min([beta, min_value])

        return min_value, alpha, beta
        ''' Max code block - checks if the state passed to it is already checked, otherwise checks the next states of passed
        state and returns the max value of those states.
        '''
    elif level == 'Max':
        for item in visitedstates:
            if CurrentState == item[1]:
                return item[0], alpha, beta
        # Get all the next states of the passed state, then compute the max of those states by passing
        # each of them
        # in turn to minimax function
        next_States = CurrentState.GetNextMoves(player)
        max_value = -math.inf
        for state in next_States:
            bestnode_State, alpha, beta = Minimax(state, 'Min', player, visitedstates, recursiondepth + 1, alpha, beta)
            max_value = max([max_value, bestnode_State])
            if max_value > beta:
                return max_value, alpha, beta
            alpha = max([alpha, max_value])
        return max_value, alpha, beta


def EvaluateState(State, player):
    '''
    :param State: State Representing the board and the pieces on it
    :param player: whether current player is w or b
    :return: single value which represents the strength of the position for the player calling the function
    '''
    strength_w = 0
    strength_b = 0

    for w in State.w_pieces:
        strength_w += len(State.board) / 2 if type(w) is Pikachu else 1
    for w in State.w_pieces:
        if w.position[0] > 0 and type(w) is pichu and State.board[w.position[0] - 1][w.position[1]] == 'w':
            strength_w += 1

    for b in State.b_pieces:
        strength_b += len(State.board) / 2 if type(b) is Pikachu else 1
    for b in State.b_pieces:
        if b.position[0] < len(State.board)-1 and type(b) is pichu and State.board[b.position[0] + 1][b.position[1]] == 'b':
            strength_b += 1
    if player == 'b':
            return len(State.b_pieces) + 0.1*strength_b + 0.1*sum([len(State.board) - b.position[0] for b in State.b_pieces]) \
               - (len(State.w_pieces) + 0.1*strength_w
                  + 0.01*sum([w.position[0] for w in State.w_pieces]))
    return len(State.w_pieces) + 0.01*strength_w  + 0.01*sum([w.position[0] for w in State.w_pieces]) \
           - (len(State.b_pieces) + 0.01*strength_b
              + 0.01*sum([len(State.board) - b.position[0] for b in State.b_pieces]))


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
    '''
    Represents an object which is a piece on the board with its color, position(row, column), character with which to represent on he board
    '''
    def __init__(self, color, position, character):
        self.color = color
        self.captured = False
        self.position = position
        self.character = character

    def findvalidmoves(self, b):
        '''

        :param b: the board State, passed to know the other pieces on the board so that
        the correct valid moves for this piece can be returned
        :return: list of (row, column) values to which piece can move
        '''
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
    '''
    Represents a Pikachu piece, with color, position(row, column), character to represent on the board
    '''
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
        '''
        :param validmoves: given the boards current piece, which are the valid directions it can move, e.g., if its at a corner, some moves are restricted
        :param b: the board state to help get the positions which are empty and can be moved to
        :return: a list of (row, column values) to which this Pikachu object can move to. computed by calling 4 different methods to check possible moves in all directions
        '''
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
    '''
    :param board: takes a board 2d list with all the characters as input in the arguments
    :param N: the dimensions of the board
    :return: for all w and b characters, return a list of pichu/Pikachu objects for both colors.
    '''
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
    moves = []
    alpha = -math.inf
    beta = math.inf
    while True:
        for next_move in current_state.GetNextMoves(player):
            move, alpha, beta = Minimax(next_move, 'Max', player, visited_states, recursiondepth, alpha, beta)
            moves.append((move, next_move))
        best_move = max(moves, key=lambda t:t[0])
        moves = []
        current_state = best_move[1]
        player = 'b' if player == 'w' else 'w'
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
    # start = time.time()
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
        # print(time.time() - start)
        # start = time.time()
