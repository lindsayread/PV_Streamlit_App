import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import re
import string
import nltk
import os

# def w2v_tokenizer(document):
#     stoplist = set('for a an it its very of the and to in'.split())
#     texts = [word for word in document.lower().split() if word not in stoplist]

# def viable_words(words):
#     viable_words = []
#     for word in words:
#         try:
#             model[word]
#             viable_words.append(word)
#         except:
#             pass
#     return viable_words

def run_nlp_portion_only(txt):
    vectors = pd.read_csv('nlp_vectors.csv')

    input_text = txt

    remove_n = lambda x: re.sub('\\n',' ',x)
    remove_singlen = lambda x: re.sub('\n',' ',x)
    alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
    punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    input_text1 = remove_n(input_text)
    input_text1 = remove_singlen(input_text1)
    input_text1 = alphanumeric(input_text1)
    input_text1 = punc_lower(input_text1)
    remove_emoji = lambda x: emoji_pattern.sub(r'', x)
    input_text1 = remove_emoji(input_text1)

    stoplist = set('for a an it its very of the and to in'.split())
    tokenized = [word for word in input_text1.lower().split() if word not in stoplist]

    google_vec_file = '/Users/lindsayread/Downloads/GoogleNews-vectors-negative300.bin'
    model = gensim.models.KeyedVectors.load_word2vec_format(google_vec_file, binary=True)

    viable_words = []
    for word in tokenized:
        try:
            model[word]
            viable_words.append(word)
        except:
            pass
    viables = viable_words

    df_first = pd.DataFrame([model[viables[0]]])
    for word in viables[1:]:
        df_first = pd.concat([df_first, pd.DataFrame([model[f'{word}']])], ignore_index=True)
    df_mean = pd.DataFrame(df_first.mean())
    text_vector = df_mean.T

    text_vector.columns = vectors.columns
    vectors_all = vectors.append(text_vector, ignore_index=True)

    similarity_matrix = pd.DataFrame(cosine_similarity(vectors_all))

    text_similarity = similarity_matrix[329][:-1]
    top3 = text_similarity.nlargest(3)
    idx_numbers = list(top3.index.values)

    all_info = pd.read_csv('all_info_cleaned.csv')
    top3df = all_info.iloc[idx_numbers,:]

    tb_returned = top3df[['name_x','rating_x','website','vicinity','international_phone_number']]
    return tb_returned
