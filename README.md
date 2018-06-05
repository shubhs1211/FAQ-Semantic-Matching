# FAQ Semantic Matching

An application that will produce improved results using NLP features and techniques. 
The project includes implementation of a bag-of-words strategy and an improved strategy using NLP features and techniques.

Input:
- Set of FAQs and Answers
- User’s input is a natural language question/statement 

Output:
- One or more FAQs and Answers that match the user’s input question/statement

Language Used: python 3.6.4
Libraries Used:
-       numpy
-       scipy
-       stanfordcorenlp
-       pysolr
-       collections
-       nltk - sent_tokenize, word_tokenize, PorterStemmer, WordNetLemmatizer          
Tools used:
-       Sublime text
-       Anaconda
-       Solr

Folder contains:
one output log file
two .py files for task2 and task4
one helper .py file internal clean function
one screenshot folder with examples
QuestionBank.txt as corpus
and TestBank.csv as test corpus with variation of corpus questions
and project report.


To Execute:

Download Solr 7.1.0 from http://www.apache.org/dyn/closer.lua/lucene/solr/7.1.0. 
- Extract solr binaries.In Navigate to solr-7.1.0 folder 
-go solr-7.1.0/bin and open file location in terminal 
- run command: solr start -p <port no.>
		run command: solr start -p 8983 (for our code)
- create a core using command: create -c <folderName>
		create a core using command: create -c task3
- open solr admin on any browser http://localhost:<portNumber>/solr/#/

Download from : http://www.nltk.org/
Stanford NLP : http://nlp.stanford.edu/software/corenlp.shtml 

go to folder location in the terminal and give the command as below to run the core nlp server on 9000 port:
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

run task4.py from command line(python) for task 3 and task4
run task2.py from command line(python) for task 2


Created by : Team Inquisitors
Group Members: Priyanka Joshi, Shubham Kothari