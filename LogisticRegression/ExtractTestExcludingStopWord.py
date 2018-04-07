
import os
from test.test_trace import my_file_and_modname
from _csv import Error

output_list = [];
Attribute_list = [[]];
negative_attribute_count = []
positive_attribute_count = []
wordlist = [];
wordcount = [];
position = 0;
row_count = 0;
Unwanted_words = {'-', ':', ',', '.', '/'}
row_values = [[]]


def Getfilesinfolder(path):
    list = []
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            list.append(dir_entry_path)
    return list;


def getDataFromFiles(list):
    data = []
    for files in list:
        with open(files, 'r') as my_file:
            try:
                s = my_file.read()
            except:
                pass
            data.append(s);
    return data;


def getSpamClassDataExcludingStopWords(list, position, stop_words):
    row_count = 1;
    row_value_temp = []
    for each_data in list:
        words_inlist = each_data.split()
        row_value_temp = []

        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
            row_values.insert(row_count - 1, row_value_temp)
        row_itteration = 0;
        for words in words_inlist:
            '''To exclude stop words'''
            try:
                stop_index = stop_words.index(words)
                continue
            except:
                pass
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
                    row_values[row_count - 1].insert(row_itteration, words)
                    Attribute_list[row_count - 1].insert(row_itteration, 1);
                    row_itteration = row_itteration + 1
            except:

                wordlist.insert(position, words)
                wordcount.insert(position, 1);
                positive_attribute_count.insert(position, 0);
                negative_attribute_count.insert(position, 1);
                row_values[row_count - 1].insert(row_itteration, words)
                Attribute_list[row_count - 1].insert(row_itteration, 1);
                position = position + 1;
                row_itteration = row_itteration + 1

        output_list.insert(row_count, "FALSE")
        row_count = row_count + 1;

    return len(list) + 1, position


def getHamClassDataExcludingStopWords(list, row_count, position, stop_words):
    row_value_temp = []
    for each_data in list:
        words_inlist = each_data.split()
        row_value_temp = []

        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
            row_values.insert(row_count - 1, row_value_temp)
        row_itteration = 0;
        for words in words_inlist:
            '''To exclude stop words'''
            try:
                stop_index = stop_words.index(words)
                continue
            except:
                pass
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
                    row_values[row_count - 1].insert(row_itteration, words)
                    Attribute_list[row_count - 1].insert(row_itteration, 1);
                    row_itteration = row_itteration + 1
            except:

                wordlist.insert(position, words)
                wordcount.insert(position, 1);
                positive_attribute_count.insert(position, 1);
                negative_attribute_count.insert(position, 0);
                row_values[row_count - 1].insert(row_itteration, words)
                Attribute_list[row_count - 1].insert(row_itteration, 1);
                position = position + 1;
                row_itteration = row_itteration + 1

        output_list.insert(row_count, "TRUE")
        row_count = row_count + 1;


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
                value = Attribute_list[i][index];
                inputvector[i].insert(j, value);
            except:
                inputvector[i].insert(j, 0)
            j = j + 1;
        i = i + 1;
        j = 0;
    return weightvector, inputvector


def test_stop(stop_word, stop_wordlist, test_ham_folder, test_spam_folder):

    spam_list = Getfilesinfolder(test_spam_folder)
    ham_list = Getfilesinfolder(test_ham_folder)
	
    spam_array = getDataFromFiles(spam_list)
    ham_array = getDataFromFiles(ham_list)
	
    row_count, position = getSpamClassDataExcludingStopWords(spam_array, 0, stop_word)
	
    getHamClassDataExcludingStopWords(ham_array, row_count, position, stop_word)
	
    weightvector, inputvector = rephraseTestData(stop_wordlist)
	
    return row_values, Attribute_list, output_list, inputvector
    