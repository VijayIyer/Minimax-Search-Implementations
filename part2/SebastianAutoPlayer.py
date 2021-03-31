# Automatic Sebastian game player
# B551 Spring 2021
# VIJAY IYER, vsiyer@iu.edu
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from SebastianState import Dice
from SebastianState import Scorecard
import random
import itertools
import math
from collections import Counter

import random
from random import randrange

class SebastianAutoPlayer:
    def __init__(self):
        self.ProbabilityMap, self.ScoreMap = GenerateProbabilityMap()

    def PredictedRolls(self, dice, subset_size, rerolled_dice):
        ''' For every choice of dice reroll a User makes, return all the possibilities with probabilities
            Parameters:
                    dice (Dice): the dice object which contains the current outcome
                    subset_size (int): no of dice for rolling again
                    rerolled_dice (list): list of indexes of the dice object whose future outcomes will be checked
            Returns:
                    predicted_dice_rolls_with_replacement (list): list of tuples containing (<predicted outcome>,
                    <probability of predicted outcome>, <indexes of dice which were rerolled for predicted outcome>)

        '''

        predicted_rolls = itertools.combinations_with_replacement(range(1, 7), subset_size)
        predicted_dice_rolls_with_replacement = []
        for roll in list(predicted_rolls):
            dice_roll = dice.dice.copy()
            i = 0
            for outcome in roll:
                dice_roll[rerolled_dice[i]] = outcome
                i += 1
            roll_string = " ".join([str(i) for i in roll])
            probability = self.ProbabilityMap[roll_string]
            d = Dice()
            d.dice = dice_roll
            predicted_dice_rolls_with_replacement.append((d, probability, rerolled_dice))
        return predicted_dice_rolls_with_replacement

    def Expectiminimax(self, dice, roll_num, scorecard, node, rerolled_dice):
        ''' Returns the best possible future outcome for a given rolled dice, with all possibilities considered
        ( 1 die rolled again, 2 dice rolled again, etc). chance nodes return expected
        value of a decision - 1st die rerolled, 2nd die rolled, 1st and 2nd die rerolled, etc. Max node picks the chance node with
        highest value, representing the best decision from that point in the tree.

        :param dice: current outcome of rolled dice
        :param roll_num: if roll_num is 3 then, we are in terminal state as per rules of the game
        :param scorecard: current scorecard, this is passed in so that categories which have already been picked are not considered
        :param node: a string making the decision whether the node is max or chance
        :param rerolled_dice: indexes of dice which
        :param terminal: a boolen flag indicating that terminal node has been reached - this is for not making recursive
        calls from a node which is not considering rerolling the dice
        :return: either a single max value containing the expected value of a decision and the index of rerolled dice if
        node is terminal, or a list of chance nodes with expected value, rerolled dice
        '''
        if roll_num == 3:
            return (self.Utility(dice, scorecard), rerolled_dice)
        elif node == 'chance':
            '''
            This is the main code block where chance nodes are generated and
            the expected value of each decision taken from a max node is returned.
            The nested for loop helps generating chance nodes for each decision - subset size decides the no. of dice to 
            be re-rolled, the range inside itertools.combinations decides which indexes will be considered for predicted 
            outcomes. Ideally subset size should be from 0 to 5 to consider the case of rerolling all the 5 dice
            However, with all combinations, for 2 layers, time being taken for single turn is way too high
            '''
            nodes = []
            predicted_rolls = []
            subset_range = range(0,2) if roll_num == 1 else range(0, 6)
            for subset_size in subset_range:
                permuations = itertools.combinations(range(0,5), subset_size)
                for rerolled_dice in permuations:
                    predicted_rolls = []
                    predicted_rolls.extend(self.PredictedRolls(dice, subset_size, list(rerolled_dice)))
                    expected_Value = 0
                    for action in predicted_rolls:
                        utility_value = self.Expectiminimax(action[0], roll_num, scorecard, 'max', action[2])[0]
                        expected_Value += utility_value*action[1]
                    nodes.insert(0,(expected_Value, rerolled_dice))
            return nodes
        else:
            max_nodes = []
            if roll_num+1 == 3:
                return self.Expectiminimax(dice, roll_num+1, scorecard, 'chance', rerolled_dice)
            else:
                for pair in self.Expectiminimax(dice, roll_num+1, scorecard, 'chance', rerolled_dice):
                    max_nodes.append(pair)

            max_value = max(max_nodes, key=lambda t:t[0])
            return max_value

    def Utility(self, dice:Dice, scorecard):
        '''
        :param dice: the outcome of the rolled dice
        :param scorecard: keeps track of which categories have already been picked and doesnt
        :return: Returns a single value which is the max score of all categories available on the scorecard for a
        single outcome of the rolled dice
        '''
        computed_scorecard = self.ScoreMap[" ".join(str(i) for i in dice.dice)]
        for key in scorecard.scorecard.keys():
            computed_scorecard.scorecard[key] = 0
        if sum([value for k, value in scorecard.scorecard.items() if k in scorecard.Numbers.keys()]) + max([value for k, value in computed_scorecard.scorecard.items() if k in scorecard.Numbers.keys()]) > 63 and not scorecard.bonusflag:
            return max(computed_scorecard.scorecard.values()) + 35
        return max(computed_scorecard.scorecard.values())

    def first_roll(self, dice, scorecard):
        # start_time = time.time()
        current_scorecard = GetAllScores(dice, scorecard)
        best_score = max(current_scorecard.scorecard.values())
        max_value = max(self.Expectiminimax(dice, 2, scorecard, 'chance',[]),key=lambda t:t[0])
        # print(f'\n{time.time() - start_time}')
        if max_value[0] > best_score:
            return max_value[1]
        else:
            return []

    def second_roll(self, dice, scorecard):
        # start_time = time.time()
        current_scorecard = GetAllScores(dice, scorecard)
        best_score = max(current_scorecard.scorecard.values())
        max_value = max(self.Expectiminimax(dice, 2, scorecard, 'chance', []), key=lambda t: t[0])
        # print(f'\n{time.time() - start_time}')
        if max_value[0] > best_score:
            return max_value[1]
        else:
            return []

    def third_roll(self, dice, scorecard):
        current_scorecard = GetAllScores(dice,scorecard)
        max_value = max(current_scorecard.scorecard.values())  # maximum value
        max_keys = [k for k, v in current_scorecard.scorecard.items() if v == max_value]  # getting all keys containing the `maximum`
        return max_keys[0]


def GetProbability(new_roll):
    '''
    param new_roll: the outcome of the rolled dice
    :return: probability of a given dice outcome, considering 1-6 is possible on a single die.
    This value is calculated considering the number of duplicate numbers in the outcome.
    '''
    cnt = Counter(new_roll)
    counts = {k: v for k, v in cnt.items() if v > 1}
    return (math.factorial(len(new_roll)) / FactorialProducts(counts)) / (6 ** len(new_roll))


def FactorialProducts(counts: dict):
    '''

    :param counts: the counts of the different numbers on the rolled die, for e.g, (1, 1, 2) then counts {is 1:2, 2:1}
    :return: product of factorials of the no. of occurences of the unique numbers in the outcome
    '''
    res = 1
    for i, v in counts.items():
        res = res * math.factorial(v)
    return res


def GetAllScores(dice, scorecard):
    '''
    Return a Scorecard for a given rolled dice with all category scores recorded so that the best one can be recorded
    taking max of all categories
    '''
    current_scorecard = Scorecard()
    allowed_Categories = set(scorecard.Categories) - set(scorecard.scorecard.keys())
    for category in allowed_Categories:
        current_scorecard.record(category, dice)
        # current_scores.append(current_scorecard)
    return current_scorecard


def ComputeExpectation(dice, subset_size, rerolled_dice):
    predicted_rolls = itertools.combinations_with_replacement(range(1,7),subset_size)
    predicted_dice_rolls_with_replacement=[]
    for roll in list(predicted_rolls):
        dice_roll = dice.dice.copy()
        i = 0
        for outcome in roll:
            dice_roll[rerolled_dice[i]] = outcome
            i += 1
        probability = GetProbability(roll)
        predicted_dice_rolls_with_replacement.append((dice_roll, probability))
    scores = []
    for predicted_roll in predicted_dice_rolls_with_replacement:
        dice_new = Dice()
        dice_new.dice = predicted_roll[0]
        scores.append((max(GetAllScores(dice_new,Scorecard()).scorecard.values()),predicted_roll[1]))
    expectation = sum([value[0]*value[1] for value in scores])
    return (subset_size, list(rerolled_dice), expectation)


def GenerateProbabilityMap():
    '''
    Pre-compute probabilities of all outcomes and keep in a dictionary so that later this value can be picked
    when a die outcome occurs
    Pre-compute Scorecards of all outcomes and keep in a dictionary so that later this value can be picked
    when a die outcome occurs

    :return: both precomputed dictionaries
    '''
    ProbabilityMap = {}
    ScoreMap = {}
    # start = time.time()
    for size in range(0, 6):
        for combination in itertools.product(range(1,7), repeat=size):
            combination_string = [str(i) for i in list(combination)]
            ProbabilityMap[" ".join(combination_string)] = GetProbability(list(combination))
            d = Dice()
            d.dice = list(combination)
            ScoreMap[" ".join(combination_string)] = GetAllScores(d,Scorecard())
    # print(time.time() - start)
    return ProbabilityMap, ScoreMap





