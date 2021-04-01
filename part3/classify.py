import sys
import math
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from collections import Counter
east_coast={}
west_coast={}
test_Labels=[]
def load_file(filename):
    objects=[]
    labels=[]
    
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
    
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to documents
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each document
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!

#
def clean_data(train_data):
    #test_data = test_data.strip( '#' ,'!','-','_','%')
    #print( len( test_data[ 'labels' ] ) , len( test_data[ 'objects' ] ) )
    unfiltered_data = train_data['objects']
    for i in range(len(unfiltered_data)):
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '#' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '!' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '@' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '$' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '%' , '' )
        unfiltered_data[i]=unfiltered_data[i].replace('.','')

        unfiltered_data[i]=unfiltered_data[i].replace('-','')
        unfiltered_data[i]=unfiltered_data[i].replace(':','')
        unfiltered_data[i]=unfiltered_data[i].replace('-','')
        unfiltered_data[i]=unfiltered_data[i].replace('--------','')
        # print( unfiltered_data)
        train_data['objects'][i] = unfiltered_data[i]
    unfiltered_data_test = test_data['objects']
    for i in range(len(unfiltered_data_test)):
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('#', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('!', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('@', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('$', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('%', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('.', '')

        unfiltered_data_test[i] = unfiltered_data_test[i].replace('-', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace(':', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('-', '')
        unfiltered_data_test[i] = unfiltered_data_test[i].replace('--------', '')
        test_data['objects'][i] = unfiltered_data_test[i]
        # print( unfiltered_data)
    return train_data, test_data

# # Open and read in a text file.
# txt_file = open("tweets.location.test.txt")
# txt_line = txt_file.read()
# txt_words = txt_line.split()
#
# # stopwords found counter.
# sw_found = 0
#
# # If each word checked is not in stopwords list,
# # then append word to a new text file.
# for check_word in txt_words:
#     if not check_word.lower() in stop_words:
#         # Not found on stopword list, so append.
#         appendFile = open('stopwords-removed.txt','a')
#         appendFile.write(" "+check_word)
#         appendFile.close()
#     else:
#         # It's on the stopword list
#         sw_found +=1
# #         print(check_word)
#
# # print(sw_found,"stop words found and removed")
# # print("Saved as 'stopwords-removed.txt' ")
#
#
   
    
        
        
   
    #print( test_data[ 'objects' ][ 0 ] )
def map_generator(train_data):
    #for i in range(len(train_data)):
    """
    for i in range(50):
        train_data[ i ] =train_data[i].split(' ')
    
        for elem in train_data[i]:
           # print(elem)
           if (elem in train_dict):
               train_dict[elem]+=1
           else:
               train_dict[elem]=1
    print(train_dict)
    """
    
    for i in range(len(train_data['objects'])):
        if(train_data['labels'][i]=="EastCoast"):
            train_data['objects'][i]=train_data['objects'][i].split()
            for elem in train_data['objects'][i]:
                if(elem in east_coast):
                    east_coast[elem]+=1
                else:
                    east_coast[elem]=1
        elif(train_data['labels'][i]=="WestCoast"):
            train_data['objects'][i]=train_data['objects'][i].split()
            for elem in train_data['objects'][i]:
                if(elem in west_coast):
                    west_coast[elem]+=1
                else:
                    west_coast[elem]=1
    # print(east_coast)
    # print(west_coast)
                
def probability(test_data, train_data, east_coast, west_coast):
    for i in range(len(test_data['objects'])):
        test_data['objects'][i] = test_data['objects'][i].split()
        # east_coast = {k: v for k, v in east_coast.items() if v > 1}
        # west_coast = {k: v for k, v in west_coast.items() if v > 1}
        alpha = 1
        ec = 1
        wc = 1
        for elem in test_data['objects'][i]:
            if elem in east_coast:
                ec *= (east_coast[elem]+alpha)/(sum(east_coast.values())+alpha*len(east_coast.keys()))
            else:
                ec *= 1 / (sum(east_coast.values())+alpha*len(east_coast.keys()))
            if elem in west_coast:
                wc *= (west_coast[elem]+alpha)/(sum(west_coast.values())+alpha*len(west_coast.keys()))
            else:
                wc *= 1 / (sum(west_coast.values())+alpha*len(west_coast.keys()))

        ECWC_count = Counter(train_data["labels"])

        ec *= ECWC_count["EastCoast"]/sum(ECWC_count.values())
        wc *= ECWC_count["WestCoast"]/sum(ECWC_count.values())
        if(ec>wc):
              test_Labels.append("EastCoast")
        else:
              test_Labels.append("WestCoast")
                  
                  
             
                  
    
     
               
            
    
    
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    # clean_data(train_data, test_data)


    train_data, test_data = clean_data(train_data)
    stop_words = set(stopwords.words('english'))
    # for i in train_data['objects']:
    #     i = [word for word in i if word not in stop_words]
    map_generator(train_data)
    probability(test_data, train_data, east_coast, west_coast)
    return test_Labels


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(train_data["classes"] != test_data["classes"] or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))

        
# clean_data( train_data , test_data )
##probability(train_data)
        
