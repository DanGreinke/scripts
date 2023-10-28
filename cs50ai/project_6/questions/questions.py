import nltk
import sys
import os
import pprint
import math
import re

FILE_MATCHES = 1
SENTENCE_MATCHES = 4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    library = dict()
    p = os.path.join(os.getcwd(),directory)
    for f in os.listdir(p):
        file = open(os.path.join(p,f),"r")
        library[f] = file.read()
    return library

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stops = nltk.corpus.stopwords.words("english")
    document = document.lower()
    tokenizer = nltk.tokenize.RegexpTokenizer(r'[a-z]+')
    return [i for i in tokenizer.tokenize(document) if i not in stops]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    doc_freq = {  
        word:math.log(len(documents) / [bool(word in documents[document]) for document in documents].count(True)) 
        for document in documents 
        for word in documents[document]
    }
    return doc_freq


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_dict = {
        file:{
            word:files[file].count(word) / len(files[file])
            for word in files[file]
        }
        for file in files
    }
    tf_idfs = {}
    for file in files:
        tf_idfs[file] = sum([tf_dict[file][word] * idfs[word] for word in query if word in file])
    #print(tf_idfs)
    return sorted(tf_idfs, key=lambda k: tf_idfs[k], reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    result = {}
    for sentence in sentences:
        result[sentence] = (sum(idfs[word] for word in query if word in sentence), count_matches(query, sentence)/len(sentence))
    #print(sentence_idfs)
    return sorted(result, key=lambda k: (result[k][0], result[k][1]), reverse=True)[:n]


def count_matches(query, sentence):
    counter = 0
    for word in query:
        if word in sentence:
            counter += 1
        else:
            continue
    return counter

if __name__ == "__main__":
    main()
