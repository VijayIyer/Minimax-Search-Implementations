**Problem 1 - Pikachu** - 
1. 

**Problem 2 - Sebastian** - 
 - 1. Problem Statement - Given a die roll in 1 of 13 turns, we need to make a decision such that obtained score is maximized across all turns. The decision is made up of 2 parts
 **no. of dice to reroll** and which **subset of dice of chosen size** to reroll. 
 - 2. To obtain the best decision, we calculate the expected value of each decision and chose the one with the maximum expected value. This is done using Expectminimax but with no min layer since this is a 1 player game. Conceptually, our game tree starts with the given roll. **The root node layer is considered the 'MAX' layer**. We then produce a chance layer with one chance node representing 1 decision. for e.g, there will be a chance node for the decision - reroll die 1, chance node for decision reroll die 1,2, reroll 0, 2, 4, etc...
 - 3. Each chance node then predicts all possible outcomes for this decision given for its root. For eg., if first roll is 1, 2, 1, 2, 3,  then the decision to roll 1st die will produce the max nodes with outcomes - [1, 2, 1, 2, 3] , [2, 2, 1, 2, 3], [3, 2, 1, 2, 3], [4, 2, 1, 2, 3], [5, 2, 1, 2, 3], [6, 2, 1, 2, 3], that is the root node outcome with only 1st die outcome changed. Similarly another chance node will have the decision - reroll 2nd die. In general, **every chance node represents a decision**. The **first chance layer represents the expected values for the 2nd roll of the dice in the same turn***. Similarly the 2nd chance layer represents, the expected values for the 3rd roll of the dice in the same turn. 
 - 4. The outcomes from the chance node will also have a probability. The max nodes generated from the chance nodes each in turn generate more chance nodes. This process from step 1 - 4 above will happen until we hit a terminal or leaf level. In our game, since we have only 3 roll of dice, at the third max layer, we will stop generating chance nodes and return a value. The value returned by a max node in our game tree will be the highest score possible from that outcome(when its combined with original outcome - that is, if original roll is 1, 1, 1, 1, 4 and we reroll the 5th die, and get 1, 1, 1, 1, 1 then the value returned by this node will be 50 (**the highest category available**). **This value is multiplied by the probability of this outcome given the dice we rolled**. For same example, if we rolled only the 5th die and obtained 1, the probability of that outcome was 1/6, since only 1 die was rolled. Similarly, for 2 dice rolled and outcome of (1,2), the probability will be 1/18 (as 1,2 and 2, 1 are same combination
  - 5. The expected value of a chance node is the expected value of all its outcomes, that is, summation of (highest value possible from the max node multiplied by its probability). 
   - 6. The max node which is the parent of the chance nodes, will pick the chance node with the highest expected value. These values get backed up as the recursion values start returning and the max node at the root picks the decision which gives the maximum expected value. This value represents the strength of the decision for the 2nd roll of the dice, thus becoming our desired decision.  
    - 7. We will also have a chance node for the decision - dont reroll the dice again, since we could have already obtained the highest value possible. This chance node will produce 1 outcome(max node), the same as its root with probability as 1. The max node generated from this will, however, again generate all possible decisions. This represents the special case where a die is rolled 1st time, no roll chosen for 2nd attempt, but a different decision chosen for the 3rd roll ( this is in practice, a redundant node, since it will always pick the choice of not rolling on the 3rd level as well,if that was in fact the correct decision to begin with for the 2nd roll)

**Implementation Details** - 


3)PROBLEM STATEMENT: The problem makes use of the concept of Naives Bayes implementation for classifying tweets and calculating the accurracy.Naive Bayes technique can be used to classify several textual objects such as documents,emails,tweets into two specific cateogories such as spam vs non spam,important vs unimportant,acceptable vs inapproriate and so on.This technique uses a "bag of words" model.In this problem we have considered a textual object D which contains words w1,w2,w3....wn. There are two classes A and B. The classifier decides which class the object belongs to. 

IMPLEMENTATION:Firstly the testing and training data has been provided to us in form of tweets with labels East Coast and West Coast. These tweets are unordered.Firstly to improve the accuracy I had cleaned the data which means I have removed the special characters,puncuations and so on. For this I stored test_data[objects] into a variable called unfiltered data. A loop has then been set to traverse through unfiltered data. When a special character or a character is observed it is replaced by ''. 

Then after the data has been cleaned the probabilty and the classification is carried about. For doing this two maps called east_coast and west_coast is created.If the test_data[labels] is east coast the element is added to the east_coast map. Similarly if thr label is west coast, it is moved to west coast map. 

After I performed this I noticedb that it wasnt accurate enough. I had obtained an accuracy of 50.1. 

After performing Laplace smoothing I got the accuracy upto 80.51 percent. 
