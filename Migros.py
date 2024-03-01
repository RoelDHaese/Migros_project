import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from copy import deepcopy
from plotly.subplots import make_subplots

#st.set_page_config(layout='wide')

################# Data


@st.cache_data
def load_data(path):
    df = pd.read_csv(path, sep = ';')
    return df

bezirke_df_raw = load_data(path="data/raw/KTZH_00000254_00001282.csv")
df = deepcopy(bezirke_df_raw)

with open("C:/Users/Roel/Desktop/Propulsion/roel-dhaese/03_Visualization/Data/data/data/GEN_A4_BEZIRKE_epsg4326.json", 'r', encoding = 'utf-8') as response:
    bezirke_map = json.load(response)


if st.checkbox("Show Dataframe"):
    st.subheader("This is our dataset:")
    st.dataframe(data=df)

bezirk_df = df.groupby(["jahr", "bezirk"],as_index=False).anzahl.sum()

bezirk_2023_df = bezirk_df[bezirk_df["jahr"] == 2023].reset_index()

df_shops = pd.read_csv("data/raw/supermarkets_df")

############## Selectbox

stores = ["All"]+sorted(pd.unique(df_shops['Name']))
#store = st.selectbox("Choose your store", stores)
store = st.selectbox("Choose your store",["All"]+sorted(pd.unique(df_shops['Name'])), index = 0)

if store == "All":
    reduced_df = df_shops
else:
    reduced_df = df_shops[df_shops["Name"] == store]


############## Map

fig2ch = px.choropleth_mapbox(bezirk_2023_df, geojson=bezirke_map, locations = 'bezirk', featureidkey= 'properties.NAME' ,
                           color = 'anzahl',
                           title = 'Population distribution in the canton of Zürich',
                           zoom = 8,
                           opacity = 0.2,
                           width = 1600,
                           height = 900,
                           center = {"lat": 47.39724, "lon": 8.61872}, 
                           hover_name = 'bezirk'
                           )

fig2sc = px.scatter_mapbox(reduced_df, lat="Latitude", lon="Longitude", zoom=8, mapbox_style = 'carto-positron', color = 'Name', 
                           color_discrete_map={"Migros":"Red","Coop":"Yellow","Aldi":"Blue", "Denner":"Green"}, hover_name = 'Name')

fig2 = make_subplots()

fig2.add_traces(fig2ch.data[0])

if store == "All":
    fig2.add_traces(fig2sc.data[0])
    fig2.add_traces(fig2sc.data[2])
    fig2.add_traces(fig2sc.data[1])
    fig2.add_traces(fig2sc.data[3])
else:
    fig2.add_traces(fig2sc.data[0])
    
        

fig2.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8.7, 
                  mapbox_center = {"lat": 47.39724, "lon": 8.61872},
                  height = 800,
                  width = 800,
                  title = 'Locations of shops projected on the population density',
                  title_font_size = 25,
                  legend_orientation = "h",
                  legend_font = dict(size = 18),
                  coloraxis_colorbar = dict(title = f'Population per discrict in 2023'))

fig2.update_coloraxes(colorscale="Viridis", reversescale = True, colorbar_title_font_size = 17, colorbar_thickness = 35, colorbar_len = 1.000005, 
                    colorbar_tickfont_size = 17)

st.plotly_chart(fig2)