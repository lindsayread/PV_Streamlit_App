import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import re
import string
import nltk
import os
from sklearn.preprocessing import StandardScaler

def run_others_only(selected_features):
    numerical_cols = ['rating_x','user_ratings_total_x']
    tb_returned_cols = ['name_x','rating_x','website','international_phone_number']
    for i in selected_features:
        if i == 'restaurants':
            numerical_cols.append('rest_mean_rating')
            numerical_cols.append('num_restaurants')
            tb_returned_cols.append('top_3_restaurants')
        if i == 'tourist_attractions':
            numerical_cols.append('tourist_mean_rating')
            numerical_cols.append('num_tourist_attract')
            tb_returned_cols.append('top_3_tourist_attract')
        if i == 'art_gallery':
            numerical_cols.append('art_gallery_mean_rating')
            numerical_cols.append('num_art_galleries')
            tb_returned_cols.append('top_3_art_galleries')
        if i == 'gyms':
            numerical_cols.append('gyms_mean_rating')
            numerical_cols.append('num_gyms')
            tb_returned_cols.append('top_3_gyms')
        if i == 'shopping_malls':
            numerical_cols.append('shopping_mean_rating')
            numerical_cols.append('num_shopping')
            tb_returned_cols.append('top_3_shopping')
        if i == 'bars':
            numerical_cols.append('bars_mean_rating')
            numerical_cols.append('num_bars')
            tb_returned_cols.append('top_3_bars')
        if i == 'casinos':
            numerical_cols.append('num_casinos')
            tb_returned_cols.append('top_casinos')
        if i == 'supermarkets':
            numerical_cols.append('supermarkets_mean_rating')
            numerical_cols.append('num_supermarkets')
            tb_returned_cols.append('top_3_supermarkets')

    no_nulls = pd.read_csv('numerical_cols.csv')
    qual_only = no_nulls[numerical_cols]

    input_fields = {}
    for i in numerical_cols:
        if i == 'user_ratings_total_x':
            input_fields[i] = 432
        elif i == 'num_restaurants':
            input_fields[i] = 48
        elif i == 'num_tourist_attract':
            input_fields[i] = 9
        elif i == 'num_art_galleries':
            input_fields[i] = 16
        elif i == 'num_gyms':
            input_fields[i] = 9
        elif i == 'num_shopping':
            input_fields[i] = 7
        elif i == 'num_bars':
            input_fields[i] = 30
        else:
            input_fields[i] = 5.0

    with_input = qual_only.append(input_fields, ignore_index=True)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(with_input)
    scaled_df = pd.DataFrame(scaled)

    similarity_matrix_others = pd.DataFrame(cosine_similarity(scaled_df))

    input_row = similarity_matrix_others[329][:-1]
    input_row_df = pd.DataFrame(input_row)

    top3_others_only = input_row.nlargest(3)
    idx_numbers = list(top3_others_only.index.values)

    all_info = pd.read_csv('all_info_cleaned.csv')
    top3df = all_info.iloc[idx_numbers,:]

    tb_returned = top3df[tb_returned_cols]
    return tb_returned
