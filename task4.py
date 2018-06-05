# -*- coding: utf-8 -*-
import sys
import pandas as pd 
from nltk import tokenize
from scipy import spatial
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import wordnet as wn
from functions import clean
import collections
import pysolr
from stanfordcorenlp import StanfordCoreNLP
from nltk.tokenize import word_tokenize
import os
java_path = "C:/Program Files/Java/jdk1.8.0_151/bin/java.exe"
os.environ['JAVAHOME'] = java_path

path_to_jar = 'stanford-parser-full-2018-02-27/stanford-parser.jar'
path_to_models_jar = 'stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar'
local_corenlp_path = r'C:\Users\priya\Dropbox\Courses\NLP\Project\stanford-corenlp-full-2018-02-27\\'
server_corenlp_path = 'http://localhost:9000/'
def tokenize_corpus(fileName):
	"""Converts the given corpus into tokens
    Splits the corpus on the basis of whitespace.

    Args:
        fileName: name of file containing corpus
    Returns:
        tokens: A list of tokens
    """
	tokens = []
	file = open(r"C:\\Users\priya\Documents\GitHub\FAQ-Semantic-Matching\QuestionBank.txt", encoding='utf-8')
	# file = open(fileName, "r")
	for token in file.read().split():
		tokens.append(token)
	file.close()
	return tokens

def create_questions_and_answers(tokens):
	w, h = 1000, 50;
	questions_list = [[0 for x in range(w)] for y in range(h)]
	answers_list = [[0 for x in range(w)] for y in range(h)]
	last_period_index = -1
	a = 0
	q = 0 
	last_punctuation = ' '
	for i in range(len(tokens)):
		flag = 0
		if(tokens[i] == '.' or tokens[i] == '!'):
			# print(" 1")
			last_period_index = i
			last_punctuation = tokens[i]

			# Add last answer
			if(last_period_index == len(tokens) - 1):
				x = 0
				
				for k in range(last_question_mark_index + 1, last_period_index):
					answers_list[a][x] = tokens[k]
					x += 1
				# print("a")
				a += 1

		if(tokens[i] == '?'):	
			# print(" 2")
			if(last_punctuation == '?'):
				for k in range(last_question_mark_index + 1, i + 1):
					questions_list[q - 1][x] = tokens[k]
					x += 1
				# print("q2")
				# q += 1
				flag = 1
			if(last_period_index > 0 and flag == 0):
				x = 0
				# print(questions_list)
				# print(last_question_mark_index)
				# print(last_period_index)
				for k in range(last_question_mark_index + 1, last_period_index):
					answers_list[a][x] = tokens[k]
					x += 1
				# print("a")
				a += 1
			last_question_mark_index = i
			last_punctuation = '?'
			if (flag == 0):
				x = 0	
				# print(answers_list)
				for k in range(last_period_index + 1, last_question_mark_index + 1):
					# print(q, x , k)
					questions_list[q][x] = tokens[k]
					x += 1
				# print("q1")

				q += 1	

	# print(last_period_index)
	# print(len(tokens))
	# print('q =', q)
	# print('a =', a)
	return questions_list, answers_list

def find_Match(qa_bag,tokens_S):
    cosine=[]
    count_dict = {}
    print("\n Task2: Naive Approach for word overlap")
    print("Words matched in question-answer pairs:")
    for i in range(len(qa_bag)):
        #cosine[i] = spatial.distance.cosine(qa_bag[i], tokens_S)
        total_matches = 0
        for k in tokens_S:
        	for j in qa_bag[i]:
        		if (k.lower() == j.lower() and k != '?'):
        			total_matches += 1
        			print(i, k.lower(),', ', end = '')

        			break
        count_dict[i] = total_matches
    print("\n\n question-answer pair: total matches")
    print(count_dict)
    return count_dict

def ranking(count_dict, merged_qa_bag):
	rank_list = []
	for key, value in sorted(count_dict.items(), key = lambda x: x[1], reverse = True):
		rank_list.append(key)

	for i in range(10):
		print('\n \nquestion-answer pair index -  ', rank_list[i],"\n",i+1,". ", merged_qa_bag[rank_list[i]])

	return rank_list

def merge(temp_qa_bag):
	merged_qa_bag = []
	for j in range(len(temp_qa_bag)):
		sentence = ""
		for i in temp_qa_bag[j]:
			sentence+=(i+ " ")
		merged_qa_bag.append(sentence)

	return merged_qa_bag

def remove_stopwords(tokens):
	sw = set(stopwords.words('english'))
	cleaned_bag = []
	# exclude = set(string.punctuation)
	# 	s = ''.join(ch for ch in s if ch not in exclude)
	for i in range(len(tokens)):
		temp_sw = []
		for word in tokens[i]:
			if word not in sw:
				temp_sw.append(word)
		cleaned_bag.append(temp_sw)

	return cleaned_bag

def extract_features1(tokens):
	sw = set(stopwords.words('english'))
	wnl = WordNetLemmatizer()
	porter = PorterStemmer()

	cleaned_bag = []
	lemmatized_bag = [] 
	stemmed_bag = []
	pos_tagged_bag = []

	for i in range(len(tokens)):
		temp_sw = []
		temp_lemma = [] 
		temp_stem = []
		
		tagged_tokens = pos_tag(tokens[i])
		tags = [x[1] for x in tagged_tokens]
		pos_tagged_bag.append(tags)

		for word in tokens[i]:
			if word not in sw:
				temp_sw.append(word)
				temp_lemma.append(wnl.lemmatize(word))
				temp_stem.append(porter.stem(word))
		cleaned_bag.append(temp_sw)
		lemmatized_bag.append(temp_lemma)
		stemmed_bag.append(temp_stem)


	return cleaned_bag, lemmatized_bag, stemmed_bag, pos_tagged_bag



def extract_features2(tokens):

	parsed_bag = []
	head_words_temp = []
	for i in range(len(tokens)):
		temp = sent_tokenize(tokens[i])
		for sentence in temp:
			head_words_temp.append(get_head_word(sentence))
		parsed_bag.append(head_words_temp)

	return parsed_bag

def get_head_word(line):
	# print(line)
	# nlp = StanfordCoreNLP(local_corenlp_path)
	nlp = StanfordCoreNLP(server_corenlp_path, port=9000)
	dep_parse = nlp.dependency_parse(line)
	''' sentence = 'workers dumped sacks into a bin'
	0 workers 1 dumped 2 sacks 3 into 4 a 5 bin 6
	Dependency Parsing:
	[(u'ROOT', 0, 2), (u'nsubj', 2, 1), (u'dobj', 2, 3), (u'case', 6, 4), (u'det', 6, 5), (u'nmod', 2, 6)]
	head word: dumped # ROOT
	'''
	text = word_tokenize(line)
	head = ''
	if len(dep_parse[0]) > 2 and dep_parse[0][0] == u'ROOT' and len(text) > 0:
		head = text[dep_parse[0][2]-1]
	return head

def get_fetures_from_wordNet(qa_bag):
	all_hypernyms = []
	all_holonyms = []
	all_meronyms = []
	all_hyponyms = []
	for i in range(len(qa_bag)):
		temp_hyponyms = []
		temp_holonyms = []
		temp_meronyms = []
		temp_hypernyms = []
		for word in qa_bag[i]:
			synset_list = wn.synsets(word)
			# print(synset_list[0])
			if(len(synset_list) > 0):
				for synset in synset_list:
					for hyponyms in synset.hyponyms():
						for lemma in hyponyms.lemmas():
							temp_hyponyms.append(lemma.name())
							if(len(temp_hyponyms)):
								break
					for holonyms in synset.part_holonyms():			
						for lemma in holonyms.lemmas():
							temp_holonyms.append(lemma.name())
							if(len(temp_holonyms)):
								break
					for meronyms in synset.part_meronyms():
						for lemma in meronyms.lemmas():
							temp_meronyms.append(lemma.name())
							if(len(temp_meronyms)):
								break
					for hypernyms in synset.hypernyms():
						for lemma in hypernyms.lemmas():
							temp_hypernyms.append(lemma.name())
							if(len(temp_hypernyms)):
								break
		all_hypernyms.append(temp_hypernyms)
		all_hyponyms.append(temp_hyponyms)
		all_holonyms.append(temp_holonyms)
		all_meronyms.append(temp_meronyms)	   
	return all_hypernyms, all_hyponyms, all_holonyms, all_meronyms

def Train_solr(qa_bag_dict, core):
        solr = pysolr.Solr('http://localhost:8983/solr/'+core)
        solr.delete(q='*:*') #deletes existing fields and data from solr
        
        solr.add(qa_bag_dict ) # indexes data into the core specified
        


def query_solr(query,core):
	solr = pysolr.Solr('http://localhost:8983/solr/' + core)
	print()
	print("\nTask 4: Solr approach")

	params = {'defType': 'dismax',
				'rows': 10,
				'start': 0,
				'qf': 'lemmas^6.0 hypernyms^5.0 head_words^5.0 stem_words^1.5',
				'sort': 'score desc',
				'fl': 'score, id, tokens'}

	results = solr.search(q=query, **params)


	# results = solr.search(q=query, sort='score desc', fl='score, id, tokens')
	# print(query)
	print("Top 10 questions matching your search")
	i = 1



	print("Question No.   Score              Content")
	for result in results:
		# print(result)
		sentence = ' '.join([str(r) for r in result['tokens']])
		print( str(i) + "\t" + result['id']+ "\t" + str(result['score']) + "\t" + sentence)
		i = i + 1
	return results

def get_dictionary(qa_set, feature_set, id):

	map = collections.OrderedDict()
	'''Build id '''
	map['id'] = id
	'''Tokenizing'''
	map['tokens'] = feature_set[0]
	'''No stopwords'''
	map['no_sw'] = feature_set[1]
	'''Lemmatize'''
	map['lemmas'] = feature_set[2]
	'''Stemming'''
	map['stem_words'] = feature_set[3]
	'''POS Tagging'''
	map['pos_tags'] = feature_set[4]
	'''Root words'''
	map['head_words'] = feature_set[5]
	'''hypernyms'''
	map['hypernyms'] = feature_set[6]
	'''hyponyms'''
	map['hyponyms'] = feature_set[7]
	'''holonyms'''
	map['holonyms'] = feature_set[8]
	'''meronyms'''
	map['meronyms'] = feature_set[9]
	return map

def get_features(input_list):
	feature_tokens = input_list
	merged_input_list = merge(input_list)
	cleaned_input_list1 = []
	
	for i in merged_input_list:
		cleaned_input_list1.append(clean(i))

	cleaned_input_list = remove_stopwords(cleaned_input_list1)
	merged_cleaned_input_list = merge(cleaned_input_list)

	feature_no_sw, feature_lemma, feature_stem, feature_pos  = extract_features1(input_list)
	feature_dp = extract_features2(merged_cleaned_input_list)
	feature_hypernyms, feature_hyponyms, feature_holonyms, feature_meronyms = get_fetures_from_wordNet(cleaned_input_list)
	query_dictionary = []
	query = []
	for i in range(len(input_list)):
		query = "tokens: " + "||".join(feature_tokens[i])
		query = query + " no_sw:" + "||".join(feature_no_sw[i])
		if(len(feature_lemma[i])>0):
			query = query + " lemmas: " + "||".join(feature_lemma[i])
		if(len(feature_stem[i])>0):
			query = query + " stem_words: " + "||".join(feature_stem[i])
		if(len(feature_pos[i])>0):
			query = query + " pos_tags: " + "||".join(feature_pos[i])
		if(len(feature_dp[i]) > 0):
			query = query + "head_words " + "||".join(feature_dp[i])
		# query = query + " head_word:" + head_word
		if(len(feature_hypernyms[i])>0):
			query = query + " hypernyms: " + "||".join(feature_hypernyms[i])
		if(len(feature_hyponyms[i])>0):
			query = query + " hyponyms: " + "||".join(feature_hyponyms[i])
		if(len(feature_holonyms[i])>0):
			query = query + " holonyms: " + "||".join(feature_holonyms[i])

		if(len(feature_meronyms[i])>0):
			query = query + " meronyms: " + "||".join(feature_meronyms[i])
		# query_dictionary.append(get_dictionary(qa_bag[i], feature_set, i))	
	print('\n\n')
	print(query)
	print()
	return query

def evaluate(results,id,task):

	i = 1
	for result in results:

		# print('id', id)
		# print(int(result['id']))
		if(task==4):
			ResultID=int(result['id'])
		if(task==2):
			ResultID=result
		if( int(id) == ResultID ):
			# print('rank', i)
			return(1.0/float(i))
		i = i + 1

	return 0


if __name__ == '__main__':

	fileName = 'QuestionBank.txt'
	tokens = tokenize_corpus(fileName)


	questions_list, answers_list = create_questions_and_answers(tokens)
	
	qa_bag = []
	for i in range(0, 50):
		questions_list[i] = list(filter((0).__ne__, questions_list[i]))
		answers_list[i] = list(filter((0).__ne__, answers_list[i]))
		qa_bag.append(questions_list[i] + answers_list[i])
	
	
	print()
	merged_qa_bag = merge(qa_bag)
	


	cleaned_bag1 = []
	for i in merged_qa_bag:
		cleaned_bag1.append(clean(i))

	cleaned_bag = remove_stopwords(cleaned_bag1)
	cleaned_merged_bag = merge(cleaned_bag)

	# print("Hello1")
	# print(merged_qa_bag[0])


	# print("Hello")
	# print(cleaned_merged_bag[0])
	# print(qa_bag[0])
	# print("Bag")

	# print(cleaned_merged_bag)

	feature_tokens = qa_bag
	feature_no_sw, feature_lemma, feature_stem, feature_pos  = extract_features1(qa_bag)
	
	feature_dp = extract_features2(cleaned_merged_bag)
	
	feature_hypernyms, feature_hyponyms, feature_holonyms, feature_meronyms = get_fetures_from_wordNet(cleaned_bag)
	

	qa_bag_dictionary = []


	for i in range(len(qa_bag)):
		feature_set = []
		feature_set.append(feature_tokens[i])
		feature_set.append(feature_no_sw[i])
		feature_set.append(feature_lemma[i])
		feature_set.append(feature_stem[i])
		feature_set.append(feature_pos[i])
		feature_set.append(feature_dp[i])
		feature_set.append(feature_hypernyms[i])
		feature_set.append(feature_hyponyms[i])
		feature_set.append(feature_holonyms[i])
		feature_set.append(feature_meronyms[i])

		qa_bag_dictionary.append(get_dictionary(qa_bag[i], feature_set, i))

	# with open("logs.txt", "a") as myfile:
 #    	myfile.write(qa_bag_dictionary)
	Train_solr(qa_bag_dictionary,'task3new2')
	
	
	# s = str(input("Enter Question: "))
	
	rr_Solr=[]
	rr_Naive=[]
	df= pd.read_csv('TestBank.csv', encoding='utf-8')

	for i in range(df.shape[0]):
		tokens_S = []
		input_list = []
		s = df['Question'][i]
		print("\nInput Question: \n", s,"\n")
		id=df['ID'][i]
		for token in s.split():
			tokens_S.append(token)
		
		count_dict = find_Match(qa_bag, tokens_S)
		result_naive=ranking(count_dict, merged_qa_bag)

		input_list = [tokens_S]
		inputQuery=get_features(input_list)
		result_solr=query_solr(inputQuery,'task3new2')
		rr_Naive.append(evaluate(result_naive,id,2))
		rr_Solr.append(evaluate(result_solr,id,4))
		
	sum_Naive=0;
	sum_Solr=0;
	print("\n\nRr_Naive: " ,rr_Naive)
	print("rr_Solr: " ,rr_Solr)

	for r in rr_Solr:
		sum_Solr=sum_Solr+r
	
	MRR_Solr=sum_Solr/len(rr_Solr)

	for r1 in rr_Naive:
		sum_Naive=sum_Naive+r1
	
	MRR_Naive=sum_Naive/len(rr_Naive)

	print("\n\nMRR Naive: ",MRR_Naive)
	print("MRR Solr: ",MRR_Solr)


















