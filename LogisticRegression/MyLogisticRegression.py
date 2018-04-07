
#Importing all the functions to main

from ExtractTrain import training, classOfEachEmail
from ExtractTest import test
from ExtractTrainExcludingStopWord import training_stop
from ExtractTestExcludingStopWord import test_stop
from LogisticRegression import calculateaccuracy, formequation
from ExtractTrain import stop_words
import sys

#Get the command line arguments

training_ham_folder=sys.argv[1]
training_spam_folder=sys.argv[2]
test_ham_folder=sys.argv[3]
test_spam_folder=sys.argv[4]
Learning_Rate=float(sys.argv[5])
Lamda=float(sys.argv[6])

print('-------------------','Running Logistic Regression with stop words included', '-------------------')

weightvector,inputvector,positive,negative,negative_attribute_count,positive_attribute_count,wordlist_train,wordcount,train_output_list=training(training_ham_folder,training_spam_folder)

wordlist_test,wordpositions,classOfEachEmail,test_attributelist=test(wordlist_train,test_ham_folder,test_spam_folder)

weight_matrix=formequation(inputvector, weightvector, train_output_list,0,15,Learning_Rate,Lamda)
logistic_accuracy=calculateaccuracy(weight_matrix,test_attributelist,classOfEachEmail)


print("\nAccuracy of Logistic Regression including stop words:", logistic_accuracy*100)


print('-------------------','Running Logistic Regression with stop words excluded','-------------------')

stop_word=stop_words("StopWords.txt")

stop_weightvector,stop_inputvector,stop_positive,stop_negative,stop_negative_attribute_count,stop_positive_attribute_count,stop_wordlist,stop_wordcount,stop_train_output_list = training_stop(stop_word,training_ham_folder,training_spam_folder)

test_wordlist,test_wordpositions,stop_output_list,stop_test_attributelist = test_stop(stop_word,stop_wordlist,test_ham_folder,test_spam_folder)

weight_matrix_stop = formequation(stop_inputvector, stop_weightvector, stop_train_output_list,0,15,Learning_Rate,Lamda)
logistic_accuracy_stop = calculateaccuracy(weight_matrix_stop,stop_test_attributelist,stop_output_list)

print("\nAccuracy of Logistic Regression excluding stop words: ", logistic_accuracy_stop*100)
