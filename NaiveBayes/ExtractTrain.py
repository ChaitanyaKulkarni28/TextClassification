
import os
from test.test_trace import my_file_and_modname
from _csv import Error

classOfEachEmail = [];
Attribute_list = [[]];
negative_attribute_count = []
positive_attribute_count = []
wordlist = [];
wordcount = [];
word_position = [];
position = 0;
row_count = 0;
Unwanted_words = {'-', ':', ',', '.', '/'}
row_values = [[]]

# Appends all file names from given folder's path

def Getfilesinfolder(path):
    fileNames = []
    for dirEntries in os.listdir(path):
        dirEntryPath = os.path.join(path,dirEntries)
        if os.path.isfile(dirEntryPath):
            fileNames.append(dirEntryPath)
    return fileNames;

# Open each file in list and read its content into data[]

def getDataFromFiles(list):
    data = []
    for files in list:
        with open(files, 'r') as myFile:
            try:
                content = myFile.read()
            except:
                pass
            data.append(content);
    return data;

# To form bag of words for spam. Here list is whole data read from all files.

def trainSpamClassData(list, position):
    
    row_count = 1;					#iterator for each mail
    row_value_temp = []
    for eachMail in list:
        #eachMail is each mail as separate and wordsInMail is array of words in particular mail
        wordsInMail = eachMail.split()
        row_value_temp = []
        row_values.insert(row_count - 1, row_value_temp)
        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
        row_iteration = 0;		#no. of words in each email
        for words in wordsInMail:

            if (len(words) <= 1) or (words == 'Subject:'):
                continue

            try:
            #finds the index and increments the repsective counts if particular word occurs in particular email
                index_location = wordlist.index(words)
                negative_attribute_count[index_location] = negative_attribute_count[index_location] + 1
                wordcount[index_location] = wordcount[index_location] + 1
                try:
                    row_index = row_values[row_count - 1].index(words)
                    Attribute_list[row_count - 1][row_index] = Attribute_list[row_count - 1][row_index] + 1
                except:
                    row_values[row_count - 1].insert(row_iteration, words)
                    Attribute_list[row_count - 1].insert(row_iteration, 1);
                    row_iteration = row_iteration + 1
            except:
                #Wordlist consists of all words and wordcount has count of all words present.
                wordlist.insert(position, words)
                wordcount.insert(position, 1);
                #Since this function is for spam, I insert 1 for negative attribute count
                positive_attribute_count.insert(position, 0);		#Stores count of words separately as they appear in spam/ham class
                negative_attribute_count.insert(position, 1);			
                row_values[row_count - 1].insert(row_iteration, words)	#Stores all words from all emails
                Attribute_list[row_count - 1].insert(row_iteration, 1);	#Stores count of words in same order as row_values 
                position = position + 1;									#num of distinct words
                row_iteration = row_iteration + 1
        #classOfEachEmail list has either True or False depends on wheter it is ham or spam
        classOfEachEmail.insert(row_count, "FALSE")
        row_count = row_count + 1;						#num of emails is row_count

    return len(list) + 1, position


def trainHamClassData(list, row_count, position):
    #Bag of words for ham
    row_value_temp = []
    for eachMail in list:
        words_inlist = eachMail.split()
        row_value_temp = []

        row_values.insert(row_count - 1, row_value_temp)

        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
        row_iteration = 0;
        for words in words_inlist:

            if (len(words) <= 1) or (words == 'Subject:'):
                continue

            try:
                index_location = wordlist.index(words)
                positive_attribute_count[index_location] = positive_attribute_count[index_location] + 1
                wordcount[index_location] = wordcount[index_location] + 1
                try:
                    row_index = row_values[row_count - 1].index(words)
                    Attribute_list[row_count - 1][row_index] = Attribute_list[row_count - 1][row_index] + 1
                except:
                    row_values[row_count - 1].insert(row_iteration, words)
                    Attribute_list[row_count - 1].insert(row_iteration, 1);
                    row_iteration = row_iteration + 1
            except:

                wordlist.insert(position, words)
                wordcount.insert(position, 1);
                positive_attribute_count.insert(position, 1);
                negative_attribute_count.insert(position, 0);
                row_values[row_count - 1].insert(row_iteration, words)
                Attribute_list[row_count - 1].insert(row_iteration, 1);
                position = position + 1;
                row_iteration = row_iteration + 1

        classOfEachEmail.insert(row_count, "TRUE")
        row_count = row_count + 1;


def rephraseTrainingData():

    inputvector = [[]]
    weightvector = [[]]
    i = 0
    j = 0
    for row in Attribute_list:
        if i >= 1:
            samplematrix = []
            weightvector.insert(i, samplematrix)
            samplevector = []
            inputvector.insert(i, samplevector)
        for word in wordlist:
            weightvector[i].insert(j, 0)
            try:
                index = row_values[i].index(word)
                value = Attribute_list[i][index];
                inputvector[i].insert(j, value);
            except:
                inputvector[i].insert(j, 0)
            j = j + 1;
        i = i + 1;
        j = 0;
    return weightvector, inputvector




def training(training_ham_folder, training_spam_folder):

    spam_list = Getfilesinfolder(training_spam_folder)
    ham_list = Getfilesinfolder(training_ham_folder)

    spam_array = getDataFromFiles(spam_list)
    ham_array = getDataFromFiles(ham_list)

    row_count, position = trainSpamClassData(spam_array, 0)
    negative = len(Attribute_list)
    trainHamClassData(ham_array, row_count, position)
    total = len(Attribute_list)
    positive = total - negative
    weightmatrix, inputmatrix = rephraseTrainingData()

    return weightmatrix, inputmatrix, positive, negative, negative_attribute_count, positive_attribute_count, wordlist, wordcount, classOfEachEmail


def stop_words(stop_wrords_file):
    stop_words_list=[]
    words_list=[]
    with open(stop_wrords_file,'r') as my_file:
                try:
                    s=my_file.read()
                    words_list=s.split()
                    for each_word in wordlist:
                        stop_words_list.append(each_word)
                except:
                    pass
    return words_list