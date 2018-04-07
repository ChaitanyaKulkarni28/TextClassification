
import math

def naivebayes_accuracy(positive, negative, negative_attribute_count, positive_attribute_count, wordlist_train,
                        wordcount, wordlist_test, wordpositions, output_list):
    i = 0
    j = 0
    
    is_positive = 0
    is_negative = 0
    total_positive = 0
    total_negative = 0
    for list in wordlist_test:
        prob_of_positive = positive / (positive + negative)
        prob_of_negative = negative / (positive + negative)
        for words in list:
            try:
                total = wordpositions[i][j]			#occurence of particular word in particular email 

            except:
                total = 0

            try:
                train_index = wordlist_train.index(words)		#wordlist with all unique words
                try:
                    total_positive = positive_attribute_count[train_index] + 1
                except:
                    total_positive = 1
                try:
                    total_negative = negative_attribute_count[train_index] + 1
                except:
                    total_negative = 1
                try:
                    train_total = wordcount[train_index] + len(wordlist_train) + 1
                except:
                    train_total = len(wordlist_train) + 1
            except:
                total_positive = 1
                total_negative = 1
                train_total = len(wordlist_train) + 1
            prob_of_positive = prob_of_positive + total * math.log2((total_positive/train_total))
            prob_of_negative = prob_of_negative + total * math.log2((total_negative/train_total))

            j = j + 1
        if prob_of_positive > prob_of_negative:
            value = "TRUE"
        else:
            value = "FALSE"

        if value == output_list[i]:
            is_positive = is_positive + 1
        else:
            is_negative = is_negative + 1

        i = i + 1
        j = 0
    return is_positive / (is_negative + is_positive)
