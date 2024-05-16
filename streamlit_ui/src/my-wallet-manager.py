"""
This script is the main script for the Streamlit app.
"""

######################
#     LIBRARIES      #
######################
import ast
import sys
import streamlit as st
import joblib
import pandas as pd
from utils.utils import read_gsheet
######################


######################
#     FUNCTIONS      #
######################
######################

######################
#        MAIN        #
######################
# Read config passed as argument
config = ast.literal_eval(sys.argv[1])

# App configuration in explorer tab
st.set_page_config(
    page_title="Spends Estimator",
    page_icon=":moneybag:",
)

# Logo as header
st.image("./streamlit_ui/images/header.png", use_column_width=True)

st.title(f"{config['appName']} :moneybag:")
st.header("Estimate your monthly spends: set your requirements \
            and check the result!")

st.write(config['appDescription'])

ws_cuentas = read_gsheet(gc_credentials=config['GoogleSheets']['credentials']['path'],
                         spreadsheet_name=config['GoogleSheets']['spreadsheetName'],
                         worksheet_name="CUENTAS_TOTALES")

st.write(ws_cuentas.acell("B2").value)

left_column, right_column = st.columns(2)
INGRESOS = left_column.slider("Earnings", 0.0, 4000.0, 2600.0)
YEAR = right_column.slider("YEAR", 2020, 2100, 2024)
MONTH = left_column.slider("MONTH", 1, 12, 7)

MODEL_NAME = st.selectbox("Estimator", ("Linear Regression", "XGBoost"))

ask_spends = st.button("Get estimated monthly spends")

if ask_spends:
    if MODEL_NAME == "Linear Regression":
        MODEL_NAME = "linearregression"
    else:
        MODEL_NAME = "xgbregressor"

    # Load model from models folder
    model = joblib.load(f"{config['Models']['path']}/{MODEL_NAME}.joblib")
    df = pd.DataFrame(
        data=[[INGRESOS, YEAR, MONTH]],
        columns=['INGRESOS', 'YEAR', 'MONTH'],
    )
    result = model.predict(df)

    if MODEL_NAME == "linearregression":
        st.write(f"The estimated spends are: {round(result[0][0], 2)}")
    else:
        st.write(f"The estimated spends are: {round(result[0], 2)}")
######################
