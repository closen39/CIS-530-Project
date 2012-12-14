CIS-530-Project
Nate Close (closen@seas.upenn.edu)
Jason Mow (jmow@seas.upenn.edu)
===============

Centrality Summarizer
---------------------
The Centrality Summarizer has the following parameters to configure it's functionality:
- Sentence Vector Feature Weight Representation
- Similarity Comparison Approach
- Sentence Length Limits (short and long)
- Redundancy Removal Approach

We chose a binary representation for sentence vector feature weight. We did this because it was the simplest to compute and yielded strong results. Our similarity approach was to use cosine similarity on the sentence vectors.

Our sentence length limit was between 15 and 50 words, tokenized by NLTK. We mitigated redundancy by rejecting any sentences with a cosine similarity greater than 0.75 with any sentence already in the summary.

The performance of our Centrality Summarizer as measured by ROUGE is below. This measurement was made by summarizing only the texts in the directory 'input/d30001t_raw'.
---------------------------------------------
./ROUGE-1.5.5.pl -c 95 -r 1000 -n 2 -m -a -l 100 -x config_test.xml 
---------------------------------------------
summaries ROUGE-1 Average_R: 0.44226 (95%-conf.int. 0.44226 - 0.44226)
summaries ROUGE-1 Average_P: 0.43689 (95%-conf.int. 0.43689 - 0.43689)
summaries ROUGE-1 Average_F: 0.43956 (95%-conf.int. 0.43956 - 0.43956)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.11414 (95%-conf.int. 0.11414 - 0.11414)
summaries ROUGE-2 Average_P: 0.11275 (95%-conf.int. 0.11275 - 0.11275)
summaries ROUGE-2 Average_F: 0.11344 (95%-conf.int. 0.11344 - 0.11344)


Topic-Word Summarizer
---------------------
The Topic-Word Summarizer has the following parameters to configure it's functionality:
- Sentence Score Normalization
- Topic Word Cutoff
- Sentence Length Limits (short and long)
- Redundancy Removal Approach

For sentence vector feature weight, we chose the third representation which calculates weight as (# of topic words / # of nonstopwords). This choice seemed most logical to us as it doesn't dilute the score with stopwords, and also normalizes for sentence length.

Topic word cutoff is default 0.1

Our sentence length limit was between 15 and 50 words, tokenized by NLTK. We mitigated redundancy by rejecting any sentences with a cosine similarity greater than 0.75 with any sentence already in the summary.

The performance of our Topic-Word Summarizer as measured by ROUGE is below. This measurement was made by summarizing only the texts in the directory 'input/d30001t_raw'.
---------------------------------------------
./ROUGE-1.5.5.pl -c 95 -r 1000 -n 2 -m -a -l 100 -x config_test.xml 
---------------------------------------------
summaries ROUGE-1 Average_R: 0.38575 (95%-conf.int. 0.38575 - 0.38575)
summaries ROUGE-1 Average_P: 0.37381 (95%-conf.int. 0.37381 - 0.37381)
summaries ROUGE-1 Average_F: 0.37969 (95%-conf.int. 0.37969 - 0.37969)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.08933 (95%-conf.int. 0.08933 - 0.08933)
summaries ROUGE-2 Average_P: 0.08654 (95%-conf.int. 0.08654 - 0.08654)
summaries ROUGE-2 Average_F: 0.08791 (95%-conf.int. 0.08791 - 0.08791)
