

def clean(tokens):
    
    # Converting all words in the tokens to lower case.
    tokens = tokens.lower()

    # Removing punctuation marks from tokens by replacing them with nothing.
    tokens = tokens.replace(".", "") 
    tokens = tokens.replace(",", "")
     
    tokens = tokens.replace("\"", "")
    tokens = tokens.replace("!", "")
    tokens = tokens.replace("?", "")
    tokens = tokens.replace("-", "")
    tokens = tokens.replace(":", "")
    tokens = tokens.replace(";", "")
    tokens = tokens.replace("#", "")
    tokens = tokens.replace("\\", "")
    tokens = tokens.replace("[", "")
    tokens = tokens.replace("]", "")
    tokens = tokens.replace("{", "")
    tokens = tokens.replace("}", "")
    tokens = tokens.replace("—", "")
    tokens = tokens.replace("'", "") 
    tokens = tokens.replace("’", "") 
    tokens = tokens.replace("“", "") 
    tokens = tokens.replace("”", "") 
    
    # Replacing '(', ')', '/' with space so as to separate words 
    tokens = tokens.replace("(", " ")
    tokens = tokens.replace(")", " ")      
    tokens = tokens.replace("/", " ")

    tokens_list = []
    for token in tokens.split():
        tokens_list.append(token)
    return tokens_list




