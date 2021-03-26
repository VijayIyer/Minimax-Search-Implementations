# classify.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, March 2021
#

import sys
import math
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
def clean_data(train_data,test_data):
    #test_data = test_data.strip( '#' ,'!','-','_','%')
    #print( len( test_data[ 'labels' ] ) , len( test_data[ 'objects' ] ) )
    unfiltered_data = test_data[ 'objects' ]
    for i in range( len( unfiltered_data ) ) :
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '#' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '!' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '@' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '$' , '' )
        unfiltered_data[ i ] = unfiltered_data[ i ].replace( '%' , '' )
        unfiltered__data[i]=unfiltered-_data[i].replace('.','')
    
        unfiltered_data[i]=unfiltered_data[i].replace('-','')
        unfiltered_data[i]=unfiltered_data[i].replace(':','')
        unfiltered__data[i]=unfiltered__data[i].replace('-','')
        print( unfiltered_data)
    unfiltered=train_data['objects']
    for j in range(len(unfiltered)):
        unfiltered[ j] = unfiltered[ j ].replace( '#' , '' )
        unfiltered[j] = unfiltered[ j ].replace( '!' , '' )
        unfiltered[ j] = unfiltered[ j].replace( '@' , '' )
        unfiltered[ j] = unfiltered[ j].replace( '$' , '' )
        unfiltered[ j] = unfiltered[ j ].replace( '%' , '' )
        unfiltered[j]=unfiltered[i].replace('.','')

        unfiltered[j]=unfiltered[j].replace('-','')
        unfiltered[j]=unfiltered[j].replace(':','')
        unfiltered[j]=unfiltered[j].replace('-','')
        print( unfiltered)
        
        
   
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
    print(east_coast)
    print(west_coast)
                
    def  probability(test_data):
      for i in range(len(test_data['objects'])):
          test_data['objects'][i]=test_data['objects'][i].split()
          ec=1
          wc=1
          for elem in test_data['objects'][i]:
              if(elem in east_coast):
                  ec*=math.exp((east_coast[elem]/sum(east_coast.values())))
              if(elem in west_coast):
                  wc*=math.exp((west_coast[elem]/sum(west_coast.values())))
    if(ec>wc):
             labels.append("EastCoast")
    else:
            labels.append("WestCoast")
                  
                  
             
                  
    
     
               
            
    
    
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    return [test_data["classes"][0]] * len(test_data["objects"])


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

        
    #clean_data( train_data , test_data )
   # probability(train_data)
        
