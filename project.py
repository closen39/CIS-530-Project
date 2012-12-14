# Jason Mow (jmow@seas.upenn.edu)
# Nate Close (closen@seas.upenn.edu)

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
    for sent in sentences:
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
            


def valid(sent, summary, vectDict):
    """checks if this sentence is valid with the current summary.
    Looks at sentence length and repetition
    """
    # check validity
    threshold = 0.6
    for sentence in summary:
        print cosine_similarity(vectDict[sent], vectDict[sentence])
        if cosine_similarity(vectDict[sent], vectDict[sentence]) > threshold:
            return False
    # check length of sentence
    minLength = 15
    maxLength = 50
    words = word_tokenize(sent)
    if len(words) > maxLength or len(words) < minLength:
        return False
    # else, must be valid
    print 'sent is valid', sent
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