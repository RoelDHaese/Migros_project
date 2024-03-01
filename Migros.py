import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import geopandas as gpd
import folium
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

bezirke_df_raw = load_data(path="./data/raw/KTZH_00000254_00001282.csv", sep = ';')
bezirke_df = deepcopy(bezirke_df_raw)

