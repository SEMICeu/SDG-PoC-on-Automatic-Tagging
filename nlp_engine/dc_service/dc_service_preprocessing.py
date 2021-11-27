import re, string

import nltk as nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

def first_clean(text: str):
    """

    :param text: str
    :return: str

    This function removes spaces and other non wanted character
    """
    return " ".join(text.split())


def preprocess(text: str):
    """

    :param text: str
    :return: str

    This function converts to lowercase, strip and remove punctuations
    """
    text = text.lower()
    text = text.strip()
    text = re.compile('<.*?>').sub('', text)
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def stopword(string: str):
    """

    :param string: str
    :return: str

    This function removes english stopwords
    """
    a = [i for i in string.split() if i not in stopwords.words('english')]
    return ' '.join(a)


def get_wordnet_pos(tag):
    """

    :param tag:
    :return:
    This function is a helper function to map NTLK position tags
    """
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatizer(string: str):
    """

    :param string:
    :return: str

    This function lemmatizes the text
    """
    # Initialize the lemmatizer
    wl = WordNetLemmatizer()

    word_pos_tags = nltk.pos_tag(word_tokenize(string))  # Get position tags
    a = [wl.lemmatize(tag[0], get_wordnet_pos(tag[1])) for idx, tag in
         enumerate(word_pos_tags)]  # Map the position tag and lemmatize the word/token
    return " ".join(a)


def tokenize(text: str):
    """

    :param text:
    :return: str

    This function tokenize a string from
    """

    return nltk.word_tokenize(text)

def dc_service_preprocessing (text: str):
    """

    :param text: str
    :return: str

    This function returns the preprocessed text from the raw text with the functions defined above
    """
    return tokenize(lemmatizer(stopword(preprocess(first_clean(text)))))


