import json

import constants as cst
import requests
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

from game_prediction.tasks.scoring import load_run_mlflow

metrics = load_run_mlflow(get_metric=True)

# Set the title of the web app page and center it
st.markdown("<h1 style='text-align: center;'>⚽ GAME PREDICTION ⚽</h1>", unsafe_allow_html=True)

colored_header(
    label="Get your favorite team next game prediction !",
    description="""The objective of this app is to get a result prediction of the game of your choice.
                    The model has been trained using results from the 2023/2024 football season.
                    The model was trained on the major top 5 leagues : France, Spain, England, Germany and Italy.
                    Thefore you can only query a prediction for a game on one of these leagues. \n

                    There are three potential predictions from the model : HOME_WIN, AWAY_WIN and DRAW.
                    """,
    color_name="blue-60",
)

st.markdown("<br>", unsafe_allow_html=True)

st.warning(
    """⚠️ This app is a machine learning project made for demonstration purposes.
           Please be cautious and do not use this app for real bets."""
)

st.markdown("<br>", unsafe_allow_html=True)

colored_header(
    label="Model metrics : ",
    description="""The below results shows model current performance on each potential model output.""",
    color_name="blue-60",
)


for label_int, label_str in cst.LABEL_CONVERTED_INV.items():
    col1, col2, col3 = st.columns(3)

    col1.metric(label=f"Precision {label_str}", value=metrics[f"metrics.precision_{label_int}"])
    col2.metric(label=f"Recall {label_str}", value=metrics[f"metrics.recall_{label_int}"])
    col3.metric(label=f"F1 Score {label_str}", value=metrics[f"metrics.f1-score_{label_int}"])

    style_metric_cards(background_color="#444444")


# Add some space for better layout
st.markdown("<br>", unsafe_allow_html=True)

colored_header(
    label="Choose the game to predict : ",
    description="""Each input are controled to avoid searching for an unexisting team name.""",
)

# Text input for choosing the home team
home_team = st.text_input("🏠 Choose the home team you want:", key="home_team", placeholder="Enter Home Team")

# Text input for choosing the away team
away_team = st.text_input("🛫 Choose the away team you want:", key="away_team", placeholder="Enter Away Team")

inputs = {"home_team": home_team.upper(), "away_team": away_team.upper()}

st.markdown("<br>", unsafe_allow_html=True)

if st.button("PREDICT"):
    # st.write("Hello")
    # res = requests.post(url="http://127.0.0.1:8000/predict", data=json.dumps(inputs))
    res = requests.post(url="http://game_prediction_api:8080/predict", data=json.dumps(inputs))
    res = json.loads(res.text)["PREDICTION"]
    st.subheader(f"🎯 Model prediction is : {res}.")
