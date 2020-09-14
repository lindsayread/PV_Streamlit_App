import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
#import gensim
import re
import string
import nltk
from p5Functions import run_nlp_portion_only
from other_features import run_others_only
import time

st.title('Hotel Recommender for Puerto Vallarta, Mexico')

st.subheader('Please describe your ideal hotel')

text = st.text_area('Example: I would like a luxurious hotel that is clean and quiet. It is important to me that the staff is friendly and attentive.')
# st.write('Your top 3 recommended hotels are:', run_nlp_portion_only(text))
# if st.button('Submit Request'):
#     with st.spinner('Please be patient as we tailor your results (this could take up to 1 minute)'):
#         time.sleep(5)
#     st.write('Your top 3 recommended hotels are:',run_nlp_portion_only(text))
# else:
#     st.write('Please submit text for request')
# st.sidebar.selectbox('Do you care more about quality or quantity for these additional nearby places?', ('Quality','Quantity','Both'))
# st.sidebar.markdown('Please rate the following as it matters to you and your vacation (0 meaning you don\'t care about this aspect; 5 meaning you care a lot about this aspect)')
st.sidebar.markdown('For the following places, please mark the ones that are important to you during your stay')

restaurants = st.sidebar.checkbox('Restaurants Nearby')
tourist_attractions = st.sidebar.checkbox('Tourist Attractions Nearby')
art_gallery = st.sidebar.checkbox('Art Galleries Nearby')
gyms = st.sidebar.checkbox('Gyms Nearby')
shopping = st.sidebar.checkbox('Shopping Malls Nearby')
bars = st.sidebar.checkbox('Bars Nearby')
casinos = st.sidebar.checkbox('Casinos Nearby')
supermarkets = st.sidebar.checkbox('Supermarkets Nearby')

selected_features = []
if restaurants:
    selected_features.append('restaurants')
if tourist_attractions:
    selected_features.append('tourist_attractions')
if art_gallery:
    selected_features.append('art_gallery')
if gyms:
    selected_features.append('gyms')
if shopping:
    selected_features.append('shopping_malls')
if bars:
    selected_features.append('bars')
if casinos:
    selected_features.append('casinos')
if supermarkets:
    selected_features.append('supermarkets')

# if st.button('Submit Request'):
#     with st.spinner('Please be patient as we tailor your results (this could take up to 1 minute)'):
#         time.sleep(5)
#     st.write('Your top 3 recommended hotels are:',run_nlp_portion_only(text, selected_features))
# else:
#     st.write('Please submit text for request')
# if st.sidebar.button('Done Selecting'):
#     #st.write('trial', selected_features)
#     st.write('Your top 3 recommended hotels are:', run_others_only(selected_features))
# else:
#     st.write('Please submit request')
