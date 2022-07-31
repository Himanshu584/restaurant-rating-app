import streamlit as st
import pandas as pd
import numpy as np
import pickle

model = pickle.load(open('model.pkl','rb'))
encoding_df = pickle.load(open('encoding_df.pkl','rb'))


def order_encoder(order):
    """will encode input values from table_book and online_order"""
    if order == "Available":
        return 1
    elif order == "Not Available":
        return 0

def value_encoder(location,rest_type,cuisines,r_type,city):
    location_ = encoding_df[encoding_df.location==location].loc_en.unique()[0]
    rest_type_ = encoding_df[encoding_df.rest_type==rest_type].rest_type_en.unique()[0]
    cuisines_ = encoding_df[encoding_df.cuisines==cuisines].cuisines_en.unique()[0]
    type_ = encoding_df[encoding_df.type==r_type].type_en.unique()[0]
    city_ = encoding_df[encoding_df.city==city].city_en.unique()[0]
    return location_,rest_type_,cuisines_,type_,city_

location_list = encoding_df['location'].unique()
rest_type_list = encoding_df['rest_type'].unique()
cuisines_list = encoding_df['cuisines'].unique()
type_list = encoding_df['type'].unique()
city_list = encoding_df['city'].unique()

# -----------app------------

st.title("RESTAURANT RATING PREDICTOR (BANGALORE)")

online_order = st.selectbox(
    'Online order',
    options={'Available','Not Available'}
)

book_table = st.selectbox(
    'Table Booking',
    options={'Available','Not Available'}
)

votes = st.number_input("Number of votes",min_value=int(0))

costfor2 = st.number_input('Cost for 2 people')

location = st.selectbox(
    "Location",
    location_list
)

rest_type = st.selectbox(
    "Restaurant type",
    rest_type_list
)

cuisines = st.selectbox(
    "Cuisines",
    cuisines_list
)

r_type = st.selectbox(
    "Type",
    type_list
)

city = st.selectbox(
    "City",
    city_list
)



if st.button('predict'):
    online_ord= order_encoder(online_order)
    table_book = order_encoder(book_table)
    num_votes = int(votes)
    cost = float(costfor2)
    en_location,en_rest_type,en_cuisine,en_type,en_city = value_encoder(location,rest_type,cuisines,r_type,city)
    model_input = [[online_ord,table_book,num_votes,cost,en_location,en_rest_type,en_cuisine,en_type,en_city]] # input for model
    prediction = np.round(model.predict(model_input)[0],1)
    st.markdown("Predicted rating :- **{}**".format(prediction))
