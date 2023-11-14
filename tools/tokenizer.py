from sentence_transformers import SentenceTransformer
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer


class Tokenizer(object):
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_tokens(self, documents):
        sentences = [documents]
        sentence_embeddings = self.model.encode(
            sentences, convert_to_tensor=True)
        encod_np_array = np.array(sentence_embeddings.tolist())
        encod_list = encod_np_array.tolist()
        return encod_list[0]


class Lematize(object):

    def __init__(self) -> None:
        nltk.download('wordnet')
        self.lematizer = WordNetLemmatizer()

    def lematize_text(self, *, text_list=None or list, text=None or str) -> list:
        if text_list == None and text == None:
            raise Exception("No text or text_list provided")
        if text_list == None:
            text_list = [text]
        lematized_list = []
        for text in text_list:
            tmp = [self.lematizer.lemmatize(word.lower())
                   for word in text.split()]
            lematized_list.append(' '.join(tmp))
        return lematized_list
