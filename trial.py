import sys
from nltk import pos_tag
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# def clean(tokens):
# 	sw = set(stopwords.words('english'))
# 	wnl = WordNetLemmatizer()
# 	for i in range(len(tokens)):
# 		tokens[i] = [word for word in tokens[i] if word not in sw]
# 	return tokens


# wnl = WordNetLemmatizer()
# print(wnl.lemmatize(['cats', 'cacti']))

print(pos_tag(["Hello"]))