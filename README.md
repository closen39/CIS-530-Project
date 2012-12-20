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
- LexRank End Criteria - < 0.001 change
- Sentence Length Limits (short and long)
- Redundancy Removal Approach

For the LexRank summarizer, we chose to use TF-IDF representation over binary representation. This produced more accurate vectors and better results from ROUGE in the summarization.

For edge similarity threshold, we chose the value of 0.01. This yielded very strong results from ROUGE, much stronger than the results from values of 0.1, 0.2, and 0.3 as suggested in the text.

Our LexRank End Criteria was set such that the iteration would end if all values changed less than 0.001 between iterations. This was a good medium between performance and getting reasonable results. Also, the results did not change much as the threshold was decreased further.

Our sentence length limit was between 15 and 50 words, tokenized by NLTK. We mitigated redundancy by rejecting any sentences with a cosine similarity greater than 0.75 with any sentence already in the summary.

The performance of our LexRank Summarizer as measured by ROUGE is below. This measurement was made by summarizing only the texts in the directory 'input/d30001t_raw'.

---------------------------------------------
summaries ROUGE-1 Average_R: 0.43243 (95%-conf.int. 0.43243 - 0.43243)
summaries ROUGE-1 Average_P: 0.41509 (95%-conf.int. 0.41509 - 0.41509)
summaries ROUGE-1 Average_F: 0.42358 (95%-conf.int. 0.42358 - 0.42358)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.11911 (95%-conf.int. 0.11911 - 0.11911)
summaries ROUGE-2 Average_P: 0.11429 (95%-conf.int. 0.11429 - 0.11429)
summaries ROUGE-2 Average_F: 0.11665 (95%-conf.int. 0.11665 - 0.11665)


These are the results when run on the full corpus (50 directories, 50 summaries)

Centrality Summarizer
---------------------
summaries ROUGE-1 Average_R: 0.30704 (95%-conf.int. 0.29517 - 0.32003)
summaries ROUGE-1 Average_P: 0.30677 (95%-conf.int. 0.29494 - 0.31955)
summaries ROUGE-1 Average_F: 0.30687 (95%-conf.int. 0.29515 - 0.31968)
---------------------------------------------
summaries ROUGE-2 Average_R: 0.04664 (95%-conf.int. 0.04004 - 0.05357)
summaries ROUGE-2 Average_P: 0.04651 (95%-conf.int. 0.04001 - 0.05331)
summaries ROUGE-2 Average_F: 0.04657 (95%-conf.int. 0.04002 - 0.05344)

Topic Word Summarizer - Updated
---------------------------------------------
topicSummaries ROUGE-1 Average_R: 0.29160 (95%-conf.int. 0.28201 - 0.30077)
topicSummaries ROUGE-1 Average_P: 0.29624 (95%-conf.int. 0.28625 - 0.30619)
topicSummaries ROUGE-1 Average_F: 0.29389 (95%-conf.int. 0.28400 - 0.30344)
---------------------------------------------
topicSummaries ROUGE-2 Average_R: 0.03547 (95%-conf.int. 0.03096 - 0.04023)
topicSummaries ROUGE-2 Average_P: 0.03609 (95%-conf.int. 0.03152 - 0.04101)
topicSummaries ROUGE-2 Average_F: 0.03577 (95%-conf.int. 0.03124 - 0.04061)