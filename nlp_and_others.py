import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import re
import string
import nltk
import os
import pydeck as pdk
from sklearn.preprocessing import StandardScaler
from tb_merged import cos_nlp, cos_others

def run_nlp_and_others(txt, selected_features):
    text_similarity = 4*(cos_nlp(txt))
    cos_combined = cos_others(selected_features)

    cos_combined['nlp_portion'] = text_similarity
    cos_combined['mean_similarity'] = (cos_combined[329] + cos_combined['nlp_portion'])/2

    top3hotels = cos_combined.nlargest(3, 'mean_similarity')
    idx_numbers = list(top3hotels.index.values)
    all_info = pd.read_csv('all_info_cleaned.csv')
    top3df = all_info.iloc[idx_numbers,:]

    tb_returned_cols = ['name_x','rating_x','website','international_phone_number']
    for i in selected_features:
        if i == 'restaurants':
            tb_returned_cols.append('top_3_restaurants')
        if i == 'tourist_attractions':
            tb_returned_cols.append('top_3_tourist_attract')
        if i == 'art_gallery':
            tb_returned_cols.append('top_3_art_galleries')
        if i == 'gyms':
            tb_returned_cols.append('top_3_gyms')
        if i == 'shopping_malls':
            tb_returned_cols.append('top_3_shopping')
        if i == 'bars':
            tb_returned_cols.append('top_3_bars')
        if i == 'casinos':
            tb_returned_cols.append('top_casinos')
        if i == 'supermarkets':
            tb_returned_cols.append('top_3_supermarkets')
    tb_returned = top3df[tb_returned_cols]
    top3df['lon'] = top3df['lng']
    coords_df = top3df[['lat','lon','name_x']]
    reindexed = tb_returned.reset_index(drop=True)

    # name_removed = tb_returned_cols.remove('name_x')
    idx_numbers = list(reindexed.index.values)
    st.write('Your Top 3 Recommended Hotels Are:')

    covidLayer = pdk.Layer(
        "ScatterplotLayer",
        data=coords_df,
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["lon", "lat"],
        get_fill_color=[252, 136, 3],
        get_line_color=[255,0,0],

    )
    text_layer = pdk.Layer("TextLayer", data=coords_df, get_position=['lon','lat'],
    get_text='name_x',get_color=[0,0,0,200],get_size=15,get_alignment_baseline='bottom',)
    r = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(latitude=20.6034, longitude=-105.2253, zoom=10),
    layers=[covidLayer,text_layer])
    st.pydeck_chart(r)

    for i in idx_numbers:
        st.write(f'**Hotel {i+1}:**',reindexed['name_x'].iloc[i])
        for j in tb_returned_cols:
            #if j == 'name_x':
                #st.write('*Name:*',reindexed['name_x'].iloc[i])
            if j == 'rating_x':
                st.write('*Hotel Rating:*',reindexed['rating_x'].iloc[i])
            elif j == 'website':
                st.write('*Website:*',reindexed['website'].iloc[i])
            elif j == 'international_phone_number':
                st.write('*Phone Number:*',reindexed['international_phone_number'].iloc[i])
            elif j == 'top_3_restaurants':
                st.write('*Top Rated Restaurants Nearby:*',reindexed['top_3_restaurants'].iloc[i])
            elif j == 'top_3_tourist_attract':
                st.write('*Top Rated Tourist Attractions Nearby:*',reindexed['top_3_tourist_attract'].iloc[i])
            elif j == 'top_3_art_galleries':
                st.write('*Top Rated Art Galleries Nearby:*',reindexed['top_3_art_galleries'].iloc[i])
            elif j == 'top_3_gyms':
                st.write('*Top Rated Gyms Nearby:*',reindexed['top_3_gyms'].iloc[i])
            elif j == 'top_3_shopping':
                st.write('*Top Rated Shopping Malls Nearby:*',reindexed['top_3_shopping'].iloc[i])
            elif j == 'top_3_bars':
                st.write('*Top Rated Bars Nearby:*',reindexed['top_3_bars'].iloc[i])
            elif j == 'top_casinos':
                st.write('*Casinos Nearby:*',reindexed['top_casinos'].iloc[i])
            elif j == 'top_3_supermarkets':
                st.write('*Supermarkets Nearby:*',reindexed['top_3_supermarkets'].iloc[i])
    st.write('      ')
        #     print(j)
        #     print('Hotel {i+1}:',
        #     df[j].iloc[i])
    # hotel1 = st.write('Hotel 1:')
    #hotel1name = st.write(reindexed['name_x'].iloc[0])
    # hotel1_info = []
    # for i in tb_returned_cols:
    #     hotel1_info.append(reindexed[i].iloc[0])

    #tb_returned['name_x'].iloc[0],

    #'Rating:',tb_returned['rating_x'].iloc[0])
    return st.write('**Enjoy your customized stay in Puerto Vallarta!**')
