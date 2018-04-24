import sys
from scipy import spatial

def tokenize_corpus(fileName):
	"""Converts the given corpus into tokens
    Splits the corpus on the basis of whitespace.

    Args:
        fileName: name of file containing corpus
    Returns:
        tokens: A list of tokens
    """
	tokens = []
	file = open(fileName, "r")
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
			last_period_index = i
			last_punctuation = tokens[i]
		if(tokens[i] == '?'):	
			if(last_punctuation == '?'):
				for k in range(last_question_mark_index + 1, i):
					questions_list[q - 1][x] = tokens[k]
					x += 1
				# q += 1
				flag = 1
			if(last_period_index > 0 and flag == 0):
				x = 0
				# print(questions_list)
				# print(last_question_mark_index)
				# print(last_period_index)
				for k in range(last_question_mark_index + 1 , last_period_index):
					answers_list[a][x] = tokens[k]
					x += 1
				a += 1
			last_question_mark_index = i
			last_punctuation = '?'
			if (flag == 0):
				x = 0	
				# print(answers_list)
				for k in range(last_period_index + 1, last_question_mark_index):
					# print(q, x , k)
					questions_list[q][x] = tokens[k]
					x += 1
				q += 1					
			if( q == 50 or a == 50):
				break		
	return questions_list, answers_list

def find_Match(qa_bag,tokens_S):
    cosine=[]
    count_list = []
    
    for i in range(len(qa_bag)):
        #cosine[i] = spatial.distance.cosine(qa_bag[i], tokens_S)
        count = 0
        for j in qa_bag[i]:
        	for k in tokens_S:
        		if (k.lower() == j.lower()):
        			count += 1
        count_list.append(count) 

    print(len(count_list), count_list)

if __name__ == '__main__':
	fileName = 'QuestionBank.txt'
	tokens = tokenize_corpus(fileName)
	# print(tokens)
	questions_list, answers_list = create_questions_and_answers(tokens)
	qa_bag = []
	for i in range(0, 50):
		questions_list[i] = list(filter((0).__ne__, questions_list[i]))
		answers_list[i] = list(filter((0).__ne__, answers_list[i]))
		qa_bag.append(questions_list[i] + answers_list[i])
	tokens_S = []
	s = str(input("Enter State value "))
	for token in s.split():
		tokens_S.append(token)
	find_Match(qa_bag, tokens_S)


	


