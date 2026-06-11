import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words=set(stopwords.words("english"))
root_word=WordNetLemmatizer()

def preprocess_text(text):
    text=text.lower()
    tokens_temp=word_tokenize(text)
    tokens1=[]
    tokens=[]
    for word in tokens_temp:
        if word not in stop_words and word.isalnum():
            tokens1.append(word)
    
    for word in tokens1:
        word=root_word.lemmatize(word)
        tokens.append(word)

    return " ".join(tokens)


        


