import numpy as np
from numpy import ndarray
import re


TOKENIZER_REGEX = re.compile(r"[^\w\s]")  

def tokenize(sentence: str): # tokeniser la phrase(enlever ponctuation, mettre en minuscule, split)
    sentence = sentence.lower()
    sentence = TOKENIZER_REGEX.sub("", sentence)
    return sentence.split()


def build_vocab(intents: dict): # creer vocab avec patterns et intents et trier
    vocab = set()
    for intent_data in intents.values():
        for pattern in intent_data["patterns"]:
            for word in tokenize(pattern):
                vocab.add(word)
    return sorted(vocab)


def bag_of_words(sentence: str, vocab: list) -> np.ndarray: # convertir phrase en vecteur binaire 
    words = tokenize(sentence)
    bag = np.zeros(len(vocab), dtype=np.float32)
    for word in words:
        if word in vocab:
            bag[vocab.index(word)] = 1.0
    return bag