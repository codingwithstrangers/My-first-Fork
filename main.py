import streamlit as st
import plotly_express as px
import pandas as pd
from pathlib import Path
import sys

#TODO allow specifying source file within the stream lit webpage

SOURCE_FILE_PATH = "sample_data.csv"

def confirm_provided_arguments():
        if Path(SOURCE_FILE_PATH).is_file():
            return SOURCE_FILE_PATH
        else:
            print("Please ensure the source file is reachable")
            print(f"{SOURCE_FILE_PATH} <-- Currently does not exist")

def read_source_file(source_data:str, unique:bool =False):
    df = pd.read_csv(source_data)
    if unique:
        df = df.drop_duplicates()
    return df

def build_streamlit_app(source_data):

    # average | max | minimum values as determined by filter
    # top 3 popular genres
    # anything else we can think of?

    st.set_page_config(page_title="BestSongEver",
                       page_icon=":bar_chart:",
                       layout="wide")

    uploaded_file = st.file_uploader("SOURCE FILE", type="csv", accept_multiple_files=False, key=None, help=None, on_change=None, args=None,
                     kwargs=None, disabled=False, label_visibility="visible")

    if uploaded_file is not None:

        source_data = pd.read_csv(uploaded_file, index_col=False)

        st.header('Summary Of Input Data')
        left_col, right_col = st.columns(2)

        with left_col:
            st.metric(label="Total Items", value=len(source_data))
        with right_col:
            st.metric(label="Total Items After Removing Duplicates:", value=len(source_data.drop_duplicates(subset=['spotify_track_id'])))

        #removing duplicates for stats view
        source_data = source_data.drop_duplicates(subset=['spotify_track_id'])

        #Filter Start
        valid_genre = ["genre_1","genre_2","genre_3","genre_4","genre_5","genre_6","genre_7","genre_8","genre_9","genre_10"]
        unique_genres = pd.unique(source_data[valid_genre].values.ravel())

        st.sidebar.header("Includes Genre:")
        wanted_genre  = st.sidebar.multiselect("Select Genre:",
                                                options=unique_genres,
                                                default=unique_genres
                                               )
        df_selection = source_data.query("genre_1 == @wanted_genre or genre_2 == @wanted_genre or genre_3 == @wanted_genre or genre_4 == @wanted_genre or genre_5 == @wanted_genre or genre_6 == @wanted_genre or genre_7 == @wanted_genre or genre_8 == @wanted_genre or genre_9 == @wanted_genre or genre_10 == @wanted_genre")

        st.header('Unique Filtered Input Data')
        st.dataframe(df_selection)

        # st.table(df_selection.dtypes)
        if wanted_genre:
            st.header('Stats Based On Filtered Data')
            st.table(df_selection[['BPM','danceability', 'energy','liveness']].describe())

            option = st.selectbox("Based on what values would you like to generate an updated dictionary for requesting a "
                                  "new list of recommendations?", ('Mean', 'Max', 'Standard Deviation'))

            # wanted_ = print(getattr(df_selection,option))
            if option == 'Mean':
                wanted_metric_bpm = df_selection['BPM'].mean()
                wanted_metric_danceability = df_selection['danceability'].mean()
                wanted_metric_energy = df_selection['energy'].mean()
                wanted_metric_liveness= df_selection['liveness'].mean()

            if option == 'Max':
                wanted_metric_bpm = df_selection['BPM'].max()
                wanted_metric_danceability = df_selection['danceability'].max()
                wanted_metric_energy = df_selection['energy'].max()
                wanted_metric_liveness= df_selection['liveness'].max()

            if option == 'Standard Deviation':
                wanted_metric_bpm = df_selection['BPM'].std()
                wanted_metric_danceability = df_selection['danceability'].std()
                wanted_metric_energy = df_selection['energy'].std()
                wanted_metric_liveness= df_selection['liveness'].std()

            if option:
                updated_dict = {'BPM': wanted_metric_bpm,
                 'danceability':wanted_metric_danceability,
                 'energy':wanted_metric_energy,
                 'liveness':wanted_metric_liveness
                 }

                st.code(f'{updated_dict}')

if __name__ == '__main__':
    #read provided file from CLI
    file_path = confirm_provided_arguments()

    # Prepares provided file for processing
    source_df = read_source_file(file_path, unique=True)

    # Drives the logic used to build our simple DB web app
    build_streamlit_app(source_df)
