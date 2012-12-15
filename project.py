# Jason Mow (jmow@seas.upenn.edu)
# Nate Close (closen@seas.upenn.edu)

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from math import sqrt

def centrality_sum(document):
    # get sentences of document
    sentences = sent_tokenize(document)
    diction = dict()
    # keeps track of vectors for each sentence
    vectDict = dict()
    # build the sentence -> centrality dictionary
    for sentence in sentences:
        sim, vect = get_sim(sentence, document)
        diction[sentence] = sim
        vectDict[sentence] = vect
    # sort sentences in decreasing order
    sorted_sents = sorted(diction.keys(), key=lambda x: diction[x], reverse=True)
    
    # create summary based on validity and a threshold
    summary = list()
    sumLength = 0
    for sent in sorted_sents:
        if valid(sent, summary, vectDict):
            sumLength += len(word_tokenize(sent))
            # break if this pushes us over the threshold
            if sumLength > 100:
                break
            # else, append and continue
            summary.append(sent)
    # construct text with sentences
    text = ""
    for summ in summary:
        text += str(summ) + " "
    return text
           
def topic_word_sum(document):
    # load topic words
    topicwords = load_topic_words('topicwords.ts')
    # read in stoplist file
    stoplistfile = open('stoplist.txt')
    stoplist = [line.strip() for line in stoplistfile]
    sentences = sent_tokenize(document)
    # dict of sentence -> TWeight
    diction = dict()
    for sent in sentences:
        words1 = [x for x in word_tokenize(sent) if x in topicwords.keys()]
        words2 = [x for x in word_tokenize(sent) if x not in stoplist]
        # option 3
        diction[sent] = float(len(words1)) / float(len(words2))
        # option 1
        #diction[sent] = len(words1)
        # option 2
        #diction[sent] = len(words1) / len(word_tokenize(sent))

    # sort sentences in decreasing order
    sorted_sents = sorted(diction.keys(), key=lambda x: diction[x], reverse=True)
    
    # make vectDict
    vectDict = makeVectDict(sentences, document)
    summary = list()
    sumLength = 0
    for sent in sorted_sents:
        if valid(sent, summary, vectDict):
            sumLength += len(word_tokenize(sent))
            # break if this pushes us over the threshold
            if sumLength > 100:
                break
            # else, append and continue
            summary.append(sent)
    # construct text with sentences
    text = ""
    for summ in summary:
        text += str(summ) + " "
    return text 

def lex_rank_sum(document):
    sentences = sent_tokenize(document)
    adjList = dict()
    currRank = dict()
    vectDict = makePageRankDict(sentences, document)
    edge_threshold = 0.1

    for idx,sent in enumerate(sentences):
        adjList[idx] = list()
        currRank[idx] = 1.0

    # Construct the Graph
    for idx,sent in enumerate(sentences):
        for idx2,sent2 in enumerate(sentences):
            if sent != sent2:
                sim = cosine_similarity(vectDict[sent], vectDict[sent2])
                if sim > edge_threshold:
                    adjList[idx].append(idx2)

    # Lex Rank
    while True:
        nextRank = dict()
        for sent,edges in adjList.iteritems():
            for sent2 in edges:
                nextRank[sent2] += float(currRank[sent]) / float(len(edges))
        if notChanging(currRank, nextRank):
            break
        else:
            currRank = nextRank

    sorted_sents = [sentences[x] for x in sorted(currRank.keys(), key=lambda x: currRank[x], reverse=True)]

    summary = list()
    sumLength = 0
    for sent in sorted_sents:
        if valid(sent, summary, vectDict):
            sumLength += len(word_tokenize(sent))
            # break if this pushes us over the threshold
            if sumLength > 100:
                break
            # else, append and continue
            summary.append(sent)
    # construct text with sentences
    text = ""
    for summ in summary:
        text += str(summ) + " "
    return text 

def notChanging(currRank, nextRank):
    threshold = 0.001
    for key,value in currRank.iteritems():
        if nextRank[key] - value > threshold:
            return False
    return True

def makePageRankDict(sentences, document):
    vecDict = dict()
    lookup = dict()
    for line in open('bgIdfValues.unstemmed.txt'):
        data = line.split(" ")
        if len(data) == 1:
            continue
        lookup[data[0]] = float(data[1])
    words = word_tokenize(document)
    for sentence in sentences:
        sent_vec = [0.0] * len(words)
        for idx, word in enumerate(words):
            if word in sentence and word.lower() in lookup:
                sent_vec[idx] = lookup[word.lower()]
        vecDict[sentence] = sent_vec
    return vecDict

def makeVectDict(sentences, document):
    vectDict = dict()
    words = word_tokenize(document)
    # make vector for sentence
    for sentence in sentences:
        sent_vec = [0] * len(words)
        for idx, word in enumerate(words):
            if word in sentence:
                # binary representation for now
                sent_vec[idx] = 1
        vectDict[sentence] = sent_vec
    return vectDict

def valid(sent, summary, vectDict):
    """checks if this sentence is valid with the current summary.
    Looks at sentence length and repetition
    """
    # check validity
    threshold = 0.75
    for sentence in summary:
        #print cosine_similarity(vectDict[sent], vectDict[sentence])
        if cosine_similarity(vectDict[sent], vectDict[sentence]) > threshold:
            return False
    # check length of sentence
    minLength = 15
    maxLength = 50
    words = word_tokenize(sent)
    if len(words) > maxLength or len(words) < minLength:
        return False
    # else, must be valid
    #print 'sent is valid', sent
    return True



def get_sim(sentence, doc):
    """ gets the centrality of sentence with every sentence in doc
    """
    sents = sent_tokenize(doc)
    words = word_tokenize(doc)
    # make vector for sentence
    sent_vec = [0] * len(words)
    for idx, word in enumerate(words):
        if word in sentence:
            # binary representation for now
            sent_vec[idx] = 1
    sum_of_sims = 0
    for sent in sents:
        # construct vector for each sentence
        if sent != sentence:
            temp_vec = [0] * len(words)
            for idx, word in enumerate(words):
                if word in sent:
                # binary representation for now
                    temp_vec[idx] = 1
            sum_of_sims += cosine_similarity(sent_vec, temp_vec)
    return sum_of_sims / len(sents), sent_vec




def cosine_similarity(x, y):
    """ from hw2 """
    prodCross = 0.0
    xSquare = 0.0
    ySquare = 0.0
    for i in range(min(len(x), len(y))):
        prodCross += x[i] * y[i]
        xSquare += x[i] * x[i]
        ySquare += y[i] * y[i]
    if (xSquare == 0 or ySquare == 0):
        return 0.0
    return prodCross / (sqrt(xSquare) * sqrt(ySquare))



def get_all_files(directory):
    """ from hw4 """
    files = PlaintextCorpusReader(directory, '.*')
    return [directory + "/" + x for x in files.fileids()]

def load_topic_words(topic_file):
    dict1 = {}
    file1 = open(topic_file)
    for line in file1:
        x = line.strip().split(' ')
        dict1[x[0]] = float(x[1])
    return dict1


if __name__ == '__main__':
    files = get_all_files('input/d30001t_raw')
    outfile = open('rouge/summaries/summary00.txt', 'w')
    for file in files:
        # summary = centrality_sum(open(file).read())
        # summary = topic_word_sum(open(file).read())
        summary = lex_rank_sum(open(file).read())
        outfile.write(summary + "\n")
    outfile.close()
