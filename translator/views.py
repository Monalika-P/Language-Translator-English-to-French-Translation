from django.shortcuts import render
import tensorflow as tf
import nltk
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from tensorflow.keras.preprocessing.text import one_hot, Tokenizer
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Create your views here.

def home(request):
    return render(request, 'Predict.html')

# Loading the translator model
def load_model():
   lang_model = tf.keras.models.load_model('eng-fre-weights.h5')
   return lang_model

# Loading the Tokenizer
def load_tokenizer():
    x_tokenizer = joblib.load('eng.pickle')
    y_tokenizer = joblib.load('frn.pickle')
    return x_tokenizer, y_tokenizer

def remove_punc(x):
  x = re.sub('[!#?,.:";]', '', x)
  return x

# function to make prediction
def prediction(x, x_tokenizer, y_tokenizer):
    lang_model = load_model()
    predictions = lang_model.predict(x)[0]
    id_to_word = {id: word for word, id in y_tokenizer.word_index.items()}
    id_to_word[0] = ''
    return ' '.join([id_to_word[j] for j in np.argmax(predictions,1)])


def tokenize_and_pad(x, maxlen):

  tokenizer = Tokenizer(char_level = False)
  tokenizer.fit_on_texts(x)
  sequences = tokenizer.texts_to_sequences(x)
  padded = pad_sequences(sequences, maxlen = maxlen, padding = 'post')
  return tokenizer, sequences, padded

def pad_to_text(padded, tokenizer):
    id_to_word = {id: word for word, id in tokenizer.word_index.items()}
    id_to_word[0] = ''
    return ' '.join([id_to_word[j] for j in padded])

def predict(request):
    if request.method == 'POST':
        text = request.POST['text']

        text = remove_punc(text)
        x_tokenizer, y_tokenizer = load_tokenizer()

        text = pad_to_text(text, x_tokenizer)