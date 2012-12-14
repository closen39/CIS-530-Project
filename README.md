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
summaries ROUGE-1 Average_R: 0.44472 (95%-conf.int. 0.44472 - 0.44472)
summaries ROUGE-1 Average_P: 0.43510 (95%-conf.int. 0.43510 - 0.43510)
summaries ROUGE-1 Average_F: 0.43986 (95%-conf.int. 0.43986 - 0.43986)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.10422 (95%-conf.int. 0.10422 - 0.10422)
summaries ROUGE-2 Average_P: 0.10194 (95%-conf.int. 0.10194 - 0.10194)
summaries ROUGE-2 Average_F: 0.10307 (95%-conf.int. 0.10307 - 0.10307)


Topic-Word Summarizer
---------------------
The Topic-Word Summarizer has the following parameters to configure it's functionality:
- Sentence Vector Feature Weight Representation
- Sentence Score Normalization
- Topic Word Cutoff
- Sentence Length Limits (short and long)
- Redundancy Removal Approach