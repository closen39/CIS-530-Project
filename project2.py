# Jason Mow (jmow@seas.upenn.edu)
# Nate Close (closen@seas.upenn.edu)

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from math import sqrt
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from string import replace
from nltk.probability import FreqDist
from random import choice, seed

def centrality_sum(dir):
    # get sentences of document
    sentences = load_collection_sentences(dir)
    words = load_collection_tokens(dir)
    diction = dict()
    # keeps track of vectors for each sentence
    vectDict = dict()
    for sentence in sentences:
        vectDict[sentence] = get_sent_vec(sentence, words)
    # build the sentence -> centrality dictionary
    for sentence in sentences:
        #sim, vect = get_sim(sentence, sentences, words)
        #diction[sentence] = sim
        #vectDict[sentence] = vect
        sim = get_sim2(sentence, vectDict)
        diction[sentence] = sim
    # sort sentences in decreasing order
    sorted_sents = sorted(diction.keys(), key=lambda x: diction[x], reverse=True)
    
    # create summary based on validity and a threshold
    summary = list()
    sumLength = 0
    for sent in sorted_sents:
        if valid(sent, summary, vectDict, 0.75):
            sumLength += len(word_tokenize(sent))
            # break if this pushes us over the threshold
            if sumLength > 200:
                break
            # else, append and continue
            summary.append(sent)
    # construct text with sentences
    text = ""
    for summ in summary:
        text += str(summ) + " "
    return text
           
def topic_word_sum(dir, ts_file):
    # load topic words
    topicwords = load_topic_words(ts_file)
    # read in stoplist file
    stoplistfile = open('stoplist.txt')
    stoplist = [line.strip() for line in stoplistfile]
    sentences = load_collection_sentences(dir)
    words = load_collection_tokens(dir)
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
    vectDict = makeVectDict(dir)
    summary = list()
    sumLength = 0
    for sent in sorted_sents:
        if valid(sent, summary, vectDict, 0.75):
            sumLength += len(word_tokenize(sent))
            # break if this pushes us over the threshold
            if sumLength > 200:
                break
            # else, append and continue
            summary.append(sent)
    # construct text with sentences
    text = ""
    for summ in summary:
        text += str(summ) + " "
    return text 

def lex_rank_sum(dir):
    sentences = load_collection_sentences(dir)
    adjList = dict()
    currRank = dict()
    vectDict = makePageRankDict(dir)
    # vectDict = makeVectDict(sentences, document)
    edge_threshold = 0.2

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
        nextRank = {i:0.0 for i in currRank.keys()}
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
        if valid(sent, summary, vectDict, 0.75):
            sumLength += len(word_tokenize(sent))
            # break if this pushes us over the threshold
            if sumLength > 200:
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

def makePageRankDict(dir):
    sentences = load_collection_sentences(dir)
    words = load_collection_tokens(dir)
    vecDict = dict()
    lookup = dict()
    for line in open('bgIdfValues.unstemmed.txt'):
        data = line.split(" ")
        if len(data) == 1:
            continue
        lookup[data[0]] = float(data[1])
    for sentence in sentences:
        sent_vec = [0.0] * len(words)
        for idx, word in enumerate(words):
            if word in sentence and word.lower() in lookup:
                sent_vec[idx] = lookup[word.lower()]
        vecDict[sentence] = sent_vec
    return vecDict

def makeVectDict(dir):
    vectDict = dict()
    words = load_collection_tokens(dir)
    sentences = load_collection_sentences(dir)
    # make vector for sentence
    for sentence in sentences:
        sent_vec = [0] * len(words)
        for idx, word in enumerate(words):
            if word in sentence:
                # binary representation for now
                sent_vec[idx] = 1
        vectDict[sentence] = sent_vec
    return vectDict

def valid(sent, summary, vectDict, threshold):
    """checks if this sentence is valid with the current summary.
    Looks at sentence length and repetition
    """
    # check validity
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


def get_sim2(sentence, vectDict):
    """gets the centrality of sentence with every sentence in vector form"""
    sum_of_sims = 0.0
    sent_vec = vectDict[sentence]
    for vec in vectDict.values():
        sim = cosine_similarity(sent_vec, vec)
        # if compared with itself, don't add
        if sim == 1:
            continue
        else:
            sum_of_sims += sim
    return sum_of_sims / len(vectDict.values())


def get_sim(sentence, sents, words):
    """ gets the centrality of sentence with every sentence in doc
    """
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

def get_sent_vec(sentence, words):
    sent_vec = [0] * len(words)
    for idx, word in enumerate(words):
        if word in sentence:
            # binary representation for now
            sent_vec[idx] = 1
    return sent_vec



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

# load all sentences in files within this drectory
# should return list of sentences
def load_collection_sentences(directory):
    files = get_all_files(directory)
    li = list()
    for f in files:
        sents = load_file_sentences(f)
        li.extend(sents)
    return li

# returns a list of all sentences in that file
def load_file_sentences(filepath):
    file1 = open(filepath)
    sent = file1.read()
    return sent_tokenize(sent)

# returns a list of all tokens in a file
def load_file_tokens(filepath):
    file1 = open(filepath)
    text = file1.read()
    return word_tokenize(text)

# load all tokens in files within this directory
# should return list of tokens
def load_collection_tokens(directory):
    files = get_all_files(directory)
    li = list()
    for f in files:
        tokens = load_file_tokens(f)
        li.extend(tokens)
    return li

def get_pos_tags(sentences):
    words = list()
    for sent in sentences:
        words.extend(word_tokenize(sent))
    tags = pos_tag(words)
    return tags

def custom_summarizer(dir, ts_file):
    """greedily takes first and last sentence and changing some nouns/verbs"""
    stoplistfile = open('stoplist.txt')
    stoplist = [line.strip() for line in stoplistfile]
    files = get_all_files(dir)
    topicwords = load_topic_words(ts_file)
    sentences = list()
    for file in files:
        temp_sents = sent_tokenize(open(file).read())
        if len(temp_sents) > 0:
            sentences.append(temp_sents[0])
            sentences.append(temp_sents[-1])

    vecDict = {x:get_sent_vec(x, load_collection_tokens(dir)) for x in sentences}
    scores = dict()
    for sent in sentences:
        scores[sent] = 0
        # Centrality metric
        sim = get_sim2(sent, vecDict)
        scores[sent] += sim
        # topic word metric
        words1 = [x for x in word_tokenize(sent) if x in topicwords.keys()]
        words2 = [x for x in word_tokenize(sent) if x not in stoplist]
        scores[sent] += float(len(words1)) / float(len(words2))

    # Compile the Summary
    sorted_sents = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    summary = list()
    sumLength = 0
    for sent in sorted_sents:
        if valid(sent, summary, vecDict, 0.75):
            sumLength += len(word_tokenize(sent))
            # break if this pushes us over the threshold
            if sumLength > 200:
                break
            # else, append and continue
            summary.append(sent)
    # construct text with sentences
    text = ""
    for summ in summary:
        text += str(summ) + " "

    # Word Replacement
    tags = get_pos_tags(summary)
    nv = get_bot_nouns_verbs(tags, get_tag_mapping('en-ptb-modified.map'), 5)
    altNouns = get_alternative_words(dir, nv[0], "noun")
    altVerbs = get_alternative_words(dir, nv[1], "verb")
    for (word, alt, lesk) in altNouns:
        text = replace(text, word, alt, 1)
    for (word, alt, lesk) in altVerbs:
        text = replace(text, word, alt, 1)

    return text

def get_bot_nouns_verbs(pos_tags, tagmap, n):
    # get_func_words('/home1/c/cis530/hw4/funcwords.txt')
    funcwords = get_func_words('funcwords.txt')
    fdNoun = FreqDist()
    fdVerb = FreqDist()
    for (word, tag) in pos_tags:
        if tagmap[tag] == "VERB" and word not in funcwords and wn.synsets(word):
            fdVerb.inc(word) 
        elif tagmap[tag] == "NOUN" and word not in funcwords and wn.synsets(word):
            fdNoun.inc(word)
    return (fdNoun.keys()[::-1][:n], fdVerb.keys()[::-1][:n])

def get_tag_mapping(map_file):
    tags = dict()
    f = open(map_file)
    for line in f:
        data = line.split("\t")
        tags[data[0]] = data[1].rstrip()
    return tags

def get_func_words(filename):
    retList = list()
    f = open(filename)
    for line in f:
        retList.append(line.rstrip())
    return retList

def get_context(dir, words):
    # funcwords = get_func_words('/home1/c/cis530/hw4/funcwords.txt')
    funcwords = get_func_words('funcwords.txt')
    sentences = load_collection_sentences(dir)
    retDict = {word:set() for word in words}
    for sent in sentences:
        for word in words:
            if word in sent and word not in funcwords:
                context = [x for x in word_tokenize(sent) if x != word]
                for x in context:
                    retDict[word].add(x)
    return retDict

def get_random_alternative(word, context, pos):
    wn_pos = wn.VERB
    if pos == "noun":
        wn_pos = wn.NOUN

    synsets = wn.synsets(word)
    print 'word is ', word, 'pos is ', pos
    best = find_best_synset(synsets, context, wn_pos)
    if best is None:
        return word
    parents = best.hypernyms()
    children = best.hyponyms()
    if len(parents) > 0:
        parent = choice(parents)
        sibs = parent.hyponyms()
        sib = choice(sibs)
        if (len(sibs) > 1):
            while sib == best:
                sib = choice(sibs)
        return sib.name.split('.')[0]
    elif len(children) > 0:
        return choice(children).name.split('.')[0]
    else:
        return best.name.split('.')[0]

def get_alternative_words(dir, wordlist, pos):
    context_dict = get_context(dir, wordlist)
    retList = list()
    for word in wordlist:
        alt = get_random_alternative(word, context_dict[word], pos)
        try:
            sim = get_lesk_similarity(word, context_dict[word], alt, context_dict[alt], pos)
        except:
            # Uses context of original word if alt word context not found
            sim = get_lesk_similarity(word, context_dict[word], alt, context_dict[word], pos)
        retList.append((word, alt, sim))
    return retList

# finds and returns best Synset object
def find_best_synset(synsets, context, pos):
    print synsets, pos, context
    synset_scores = dict()
    for synset in synsets:
        if synset.pos != pos:
            continue
        vec = [0] * len(context)
        context_vec = [1] * len(context)
        definition = synset.definition.lower()
        for idx, word in enumerate(context):
            if word in definition:
                vec[idx] = 1
        #generate cosine similarity
        synset_scores[synset] = cosine_similarity(vec, context_vec)
    if len(synset_scores) == 0:
        return None
    #print "synset_scores", synset_scores
    return max(synset_scores.items(), key=lambda x: x[1])[0]

def get_lesk_similarity(word1, context1, word2, context2, pos):
    wn_pos = wn.VERB
    if pos == 'noun':
        wn_pos = wn.NOUN
    # get synsets
    synset1 = wn.synsets(word1, wn_pos)
    synset2 = wn.synsets(word2, wn_pos)
    # print "synset1 = ", synset1, "word1 = ", word1, "pos = ", pos
    # print "synset2 = ", synset2, "word2 = ", word2, "pos = ", pos
    best1 = find_best_synset(synset1, context1, wn_pos)
    best2 = find_best_synset(synset2, context2, wn_pos)
    if best1 is None or best2 is None:
        return 0
    #get hyponym glosses
    gloss1 = best1.definition
    hyp1 = best1.hyponyms()
    for hyp in hyp1:
        gloss1 += " " + str(hyp.definition)
    gloss2 = best2.definition
    hyp2 = best2.hyponyms()
    for hyp in hyp2:
        gloss2 += " " + str(hyp.definition)
    return calc_gloss_sim(gloss1, gloss2)

def calc_gloss_sim(gloss1, gloss2):
    count = 0
    visited = set(get_func_words('funcwords.txt'))
    # calculate length 2
    gloss1_list = word_tokenize(gloss1)
    for idx, word in enumerate(gloss1_list):
        if idx + 1 < len(gloss1_list) and word not in visited and gloss1_list[idx + 1] not in visited:
            if str(word) + " " + str(gloss1_list[idx + 1]) in gloss2:
                count += 4
                visited.add(word)
                visited.add(gloss1_list[idx + 1])
    # calculate length 1
    for word in word_tokenize(gloss1):
        if word not in visited and word in gloss2:
            count += 1
            visited.add(word)
    return count


if __name__ == '__main__':
    filepaths = ['input/d30001t_raw', 'input/d30002t_raw', 'input/d30003t_raw', 'input/d30005t_raw',
    'input/d30006t_raw', 'input/d30007t_raw', 'input/d30008t_raw', 'input/d30010t_raw', 'input/d30011t_raw', 
    'input/d30015t_raw', 'input/d30017t_raw', 'input/d30020t_raw', 'input/d30022t_raw', 'input/d30024t_raw',
    'input/d30026t_raw', 'input/d30027t_raw', 'input/d30028t_raw', 'input/d30029t_raw', 'input/d30031t_raw',
    'input/d30033t_raw', 'input/d30034t_raw', 'input/d30036t_raw', 'input/d30037t_raw', 'input/d30038t_raw',
    'input/d30040t_raw', 'input/d30042t_raw', 'input/d30044t_raw', 'input/d30045t_raw', 'input/d30046t_raw',
    'input/d30047t_raw', 'input/d30048t_raw', 'input/d30049t_raw', 'input/d30050t_raw', 'input/d30051t_raw',
    'input/d30053t_raw', 'input/d30055t_raw', 'input/d30056t_raw', 'input/d30059t_raw', 'input/d31001t_raw',
    'input/d31008t_raw', 'input/d31009t_raw', 'input/d31013t_raw', 'input/d31022t_raw', 'input/d31026t_raw',
    'input/d31031t_raw', 'input/d31032t_raw', 'input/d31033t_raw', 'input/d31038t_raw', 'input/d31043t_raw',
    'input/d31050t_raw']
    for idx, path in enumerate(filepaths):
        #files = get_all_files(path)
        num = "0" + str(idx)
        if idx > 9:
            num = idx
        outfile = open('rouge/summaries2/summary' + str(num) + '.txt', 'w')            
        # summary = centrality_sum(path)
        summary = topic_word_sum(path, 'tws/topic' + str(idx) + '.ts')
        # summary = lex_rank_sum(path)
        outfile.write(summary + "\n")
        outfile.close()


        # files = get_all_files('input/d30001t_raw')
        # outfile = open('rouge/summaries/summary00.txt', 'w')
        # for file in files:
        #     # summary = centrality_sum(open(file).read())
        #     # summary = topic_word_sum(open(file).read())
        #     summary = lex_rank_sum(open(file).read())
        #     outfile.write(summary + "\n")
        # outfile.close()
