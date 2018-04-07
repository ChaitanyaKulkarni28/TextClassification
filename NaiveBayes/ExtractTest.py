
import os
from test.test_trace import my_file_and_modname
from _csv import Error

output_list = [];
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


def Getfilesinfolder(path):
    fileNames = []
    for dirEntries in os.listdir(path):
        dirEntryPath = os.path.join(path,dirEntries)
        if os.path.isfile(dirEntryPath):
            fileNames.append(dirEntryPath)
    return fileNames;


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


def getSpamClassData(list, position):
    row_count = 1;
    row_value_temp = []
    for eachMail in list:
        wordsInMail = eachMail.split()
        row_value_temp = []

        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
            row_values.insert(row_count - 1, row_value_temp)
        row_iteration = 0;
        for words in wordsInMail:

            if (len(words) <= 1) or (words == 'Subject:'):
                continue

            try:

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

                wordlist.insert(position, words)
                wordcount.insert(position, 1);
                positive_attribute_count.insert(position, 0);
                negative_attribute_count.insert(position, 1);
                row_values[row_count - 1].insert(row_iteration, words)
                Attribute_list[row_count - 1].insert(row_iteration, 1);
                position = position + 1;
                row_iteration = row_iteration + 1

        output_list.insert(row_count, "FALSE")
        row_count = row_count + 1;

    return len(list) + 1, position


def getHamClassData(list, row_count, position):
    row_value_temp = []
    for eachMail in list:
        wordsInMail = eachMail.split()
        row_value_temp = []

        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
            row_values.insert(row_count - 1, row_value_temp)
        row_iteration = 0;
        for words in wordsInMail:

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

        output_list.insert(row_count, "TRUE")
        row_count = row_count + 1;

# Ignoring words which were not learned

def rephraseTestData(wordlist_test):
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
        for word in wordlist_test:
            weightvector[i].insert(j, 0)
            try:
                index = row_values[i].index(word)
                value = Attribute_list[i][index]
                inputvector[i].insert(j, value)
            except:
                inputvector[i].insert(j, 0)
            j = j + 1
        i = i + 1
        j = 0
    return weightvector, inputvector


def test(wordlist_test, test_ham_folder, test_spam_folder):

    spam_list = Getfilesinfolder(test_spam_folder);
    ham_list = Getfilesinfolder(test_ham_folder);

    spam_array = getDataFromFiles(spam_list)
    ham_array = getDataFromFiles(ham_list)

    row_count, position = getSpamClassData(spam_array, 0)
    getHamClassData(ham_array, row_count, position)
    weightvector, inputvector = rephraseTestData(wordlist_test)

    return row_values, Attribute_list, output_list, inputvector
