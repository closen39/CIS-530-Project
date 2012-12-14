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

Topic Word Cutoff was set to 12.5. We deemed this to be an optimal setting after testing out the results on several different cutoff thresholds.

Our sentence length limit was between 15 and 50 words, tokenized by NLTK. We mitigated redundancy by rejecting any sentences with a cosine similarity greater than 0.75 with any sentence already in the summary.

The performance of our Topic-Word Summarizer as measured by ROUGE is below. This measurement was made by summarizing only the texts in the directory 'input/d30001t_raw'. As stated, we chose 12.5 as our final Topic Word threshold as it yielded the best data from ROUGE.

0.1
---------------------------------------------
summaries ROUGE-1 Average_R: 0.37838 (95%-conf.int. 0.37838 - 0.37838)
summaries ROUGE-1 Average_P: 0.38500 (95%-conf.int. 0.38500 - 0.38500)
summaries ROUGE-1 Average_F: 0.38166 (95%-conf.int. 0.38166 - 0.38166)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.07692 (95%-conf.int. 0.07692 - 0.07692)
summaries ROUGE-2 Average_P: 0.07828 (95%-conf.int. 0.07828 - 0.07828)
summaries ROUGE-2 Average_F: 0.07759 (95%-conf.int. 0.07759 - 0.07759)

10.0:
---------------------------------------------
summaries ROUGE-1 Average_R: 0.40541 (95%-conf.int. 0.40541 - 0.40541)
summaries ROUGE-1 Average_P: 0.39663 (95%-conf.int. 0.39663 - 0.39663)
summaries ROUGE-1 Average_F: 0.40097 (95%-conf.int. 0.40097 - 0.40097)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.10918 (95%-conf.int. 0.10918 - 0.10918)
summaries ROUGE-2 Average_P: 0.10680 (95%-conf.int. 0.10680 - 0.10680)
summaries ROUGE-2 Average_F: 0.10798 (95%-conf.int. 0.10798 - 0.10798)

12.5
---------------------------------------------
summaries ROUGE-1 Average_R: 0.43735 (95%-conf.int. 0.43735 - 0.43735)
summaries ROUGE-1 Average_P: 0.42381 (95%-conf.int. 0.42381 - 0.42381)
summaries ROUGE-1 Average_F: 0.43047 (95%-conf.int. 0.43047 - 0.43047)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.10670 (95%-conf.int. 0.10670 - 0.10670)
summaries ROUGE-2 Average_P: 0.10337 (95%-conf.int. 0.10337 - 0.10337)
summaries ROUGE-2 Average_F: 0.10501 (95%-conf.int. 0.10501 - 0.10501)

15.0
---------------------------------------------
summaries ROUGE-1 Average_R: 0.42506 (95%-conf.int. 0.42506 - 0.42506)
summaries ROUGE-1 Average_P: 0.42402 (95%-conf.int. 0.42402 - 0.42402)
summaries ROUGE-1 Average_F: 0.42454 (95%-conf.int. 0.42454 - 0.42454)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.10670 (95%-conf.int. 0.10670 - 0.10670)
summaries ROUGE-2 Average_P: 0.10644 (95%-conf.int. 0.10644 - 0.10644)
summaries ROUGE-2 Average_F: 0.10657 (95%-conf.int. 0.10657 - 0.10657)

LexPageRank Summarizer
---------------------
The LexPageRank Summarizer has the following parameters to configure it's functionality:
- Edge Similarity Threshold
- LexRank End Criteria
- Sentence Length Limits (short and long)
- Redundancy Removal Approach

