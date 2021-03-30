3)PROBLEM STATEMENT: The problem makes use of the concept of Naives Bayes implementation for classifying tweets and calculating the accurracy.Naive Bayes technique can be used to classify several textual objects such as documents,emails,tweets into two specific cateogories such as spam vs non spam,important vs unimportant,acceptable vs inapproriate and so on.This technique uses a "bag of words" model.In this problem we have considered a textual object D which contains words w1,w2,w3....wn. There are two classes A and B. The classifier decides which class the object belongs to. 

IMPLEMENTATION:Firstly the testing and training data has been provided to us in form of tweets with labels East Coast and West Coast. These tweets are unordered.Firstly to improve the accuracy I had cleaned the data which means I have removed the special characters,puncuations and so on. For this I stored test_data[objects] into a variable called unfiltered data. A loop has then been set to traverse through unfiltered data. When a special character or a character is observed it is replaced by ''. 

Then after the data has been cleaned the probabilty and the classification is carried about. For doing this two maps called east_coast and west_coast is created.If the test_data[labels] is east coast the element is added to the east_coast map. Similarly if thr label is west coast, it is moved to west coast map. 

After I performed this I noticedb that it wasnt accurate enough. I had obtained an accuracy of 50.1. 

After performing Laplace smoothing I got the accuracy upto 80.51 percent. 
