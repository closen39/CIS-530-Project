import subprocess

def genTopicWords():
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
        text = """==== Do not change these values ====
stopFilePath = stoplist-smart-sys.txt
performStemming = N
backgroundCorpusFreqCounts = bgCounts-Giga.txt
topicWordCutoff = 0.1

==== Directory to compute topic words on ====
inputDir = /home1/c/cis530/final_project/"""

        text += path + "/\n"

        text += """==== Output File ====
outputFile = /home1/j/jmow/school/cis530/project/tws/"""
        text += "topic" + str(idx) + ".ts"
        out = open("/home1/j/jmow/school/cis530/project/configs/config" + str(idx) + ".example", "w")
        out.write(text)
        out.flush()
        out.close()

if __name__ == '__main__':
    genTopicWords()