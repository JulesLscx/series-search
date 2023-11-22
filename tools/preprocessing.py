from nltk.stem import WordNetLemmatizer
from unidecode import unidecode as remove_accents
import string


def lemma(text: list) -> list:
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text]
    return text

def remove_all_accents(text: list) -> list:
    result = [remove_accents(word) for word in text]
    return result
def remove_ponctuation(text: str) -> str:
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text        

class StopWords:
    stop_words = set()
    PATH_EN = "./tools/stopwords/stop_words_english.txt"
    PATH_FR = "./tools/stopwords/stop_words_french.txt"
    instance = None
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(StopWords, cls).__new__(cls)
            cls.instance.load_stop_words()
            print("\nStop words loaded")
        return cls.instance

    def load_stop_words(self):
        loaded = []
        with open(self.PATH_EN, 'r', encoding='utf-8') as f:
            loaded += f.read().split("\n")
        with open(self.PATH_FR, 'r', encoding='utf-8') as f:
            loaded += f.read().split("\n")
        for word in loaded:
            tmp = word.lower()
            tmp = remove_accents(tmp)
            tmp = remove_ponctuation(tmp)
            self.stop_words.add(tmp)
        
    def is_a_stop_word(self, word: str) -> bool:
        return word in self.stop_words

    def remove_stop_words(self, text: list) -> list:
        text = [word for word in text if not self.is_a_stop_word(word)]
        return text

def preprocess(text: str) -> str:
    stopwords = StopWords()
    text = remove_ponctuation(text)
    text = text.lower()
    text = text.split()
    text = remove_all_accents(text)
    text = stopwords.remove_stop_words(text)
    text = lemma(text)
    text = " ".join(text)
    return text