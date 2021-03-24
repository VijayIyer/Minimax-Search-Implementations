# Automatic Sebastian game player
# B551 Fall 2020
# PUT YOUR NAME AND USER ID HERE!
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


class SebastianAutoPlayer:

    def __init__(self):
        pass

    def first_roll(self, dice, scorecard):
        current_scorecard = GetBestScore(dice, scorecard)
        best_score = max(current_scorecard.scorecard.values())
        # newscores1 = Successors(dice)         # expectations after 1st reroll
        # newscores1 = sorted(newscores1,key=lambda t:t.difference[1])
        # best_score1 = newscores1[0]
        Expectation = [[0, [], best_score]]
        for subset_size in range(1, 5):
            permuations = itertools.combinations(range(0, 5), subset_size)
            for rerolled_dice in permuations:
                Expectation.append(ComputeExpectation(dice, subset_size, list(rerolled_dice)))
        best_reroll = max(Expectation,key=lambda t:t[2])
        if best_reroll[2] > best_score:
            return best_reroll[1]
        return []  # always re-roll first die (blindly)

    def second_roll(self, dice, scorecard):
        current_scorecard = GetBestScore(dice, scorecard)
        best_score = max(current_scorecard.scorecard.values())
        Expectation = [[0, [], best_score]]
        for subset_size in range(1, 5):
            permuations = itertools.combinations(range(0, 5), subset_size)
            for rerolled_dice in permuations:
                Expectation.append(ComputeExpectation(dice, subset_size, list(rerolled_dice)))
        best_reroll = max(Expectation, key=lambda t: t[2])
        if best_reroll[2] > best_score:
            return best_reroll[1]
        return []  # always re-roll second and third dice (blindly)

    def third_roll(self, dice, scorecard):
        # stupidly just randomly choose a category to put this in
        current_scorecard = GetBestScore(dice,scorecard)
        max_value = max(current_scorecard.scorecard.values())  # maximum value
        max_keys = [k for k, v in current_scorecard.scorecard.items() if v == max_value]  # getting all keys containing the `maximum`
        return max_keys[0]


class Die_Roll:
    def __init__(self, roll, score, dice):
        self.roll = roll
        self.score = score
        self.probability = 1
        self.original_roll = dice
        self.difference = self.differences()
        self.expectation = self.score.totalscore

    def expectations(self):
        self.expectation = self.score.totalscore * self.probability
        return self.expectation

    def differences(self):
        rerolled_dice = []
        roll_temp = self.roll.copy()
        roll_temp2 = self.original_roll.copy()

        for item1_index in range(len(self.original_roll)):
            if self.original_roll[item1_index] in roll_temp:
                roll_temp.remove(self.original_roll[item1_index])
                rerolled_dice.extend([item1_index])
                roll_temp2.remove(self.original_roll[item1_index])
        rerolled_dice = list(set(range(0, 5)) - set(rerolled_dice))
        return [roll_temp, len(roll_temp), rerolled_dice]


def Successors(dice: Dice):
    # successors = []
    # newrolls = []
    # if subset_size == 1:
    #       for i in range(0, len(dice.dice)):
    #             for j in range(1, 7):
    #                   newroll = dice.dice.copy()
    #                   newroll.pop(i)
    #                   newroll.insert(i, j)
    #                   newrolls.append(newroll)
    #
    # else:
    #       new_rolls = itertools.combinations_with_replacement([i for i in range(1, 7)], subset_size)
    # return new_rolls
    new_rolls = []
    for die_roll in itertools.combinations_with_replacement(range(1, 7), len(dice.dice)):
        new_rolls.append(list(die_roll))
    die_rolls = []
    for roll in new_rolls:
        die_roll = Dice()
        die_roll.dice = roll
        die_rolls.append(Die_Roll(die_roll.dice, GetBestScore(die_roll, Scorecard()), dice.dice))
    for die_roll in die_rolls:
        die_roll.probability = GetProbability(die_roll)
        die_roll.expectation = die_roll.probability * die_roll.score.totalscore
    return die_rolls


def GetProbability(new_roll):
    cnt = Counter(new_roll)
    counts = {k: v for k, v in cnt.items() if v > 1}
    return (math.factorial(len(new_roll)) / FactorialProducts(counts)) / (6 ** len(new_roll))


def FactorialProducts(counts: dict):
    res = 1
    for i, v in counts.items():
        res = res * math.factorial(v)
    return res


def GetBestScore(dice, scorecard):
    current_scorecard = Scorecard()
    allowed_Categories = set(scorecard.Categories) - set(scorecard.scorecard.keys())
    for categories in allowed_Categories:

        current_scorecard.record(categories, dice)
        # current_scores.append(current_scorecard)
    return current_scorecard


#
# def getdifferences(roll, original_roll):
#
#
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
        scores.append((max(GetBestScore(dice_new,Scorecard()).scorecard.values()),predicted_roll[1]))
    expectation = sum([value[0]*value[1] for value in scores])
    return (subset_size, list(rerolled_dice), expectation)

