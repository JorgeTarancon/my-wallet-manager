######################
#     LIBRARIES      #
######################
import ast
import streamlit as st
import sys
import gspread
import joblib
import pandas as pd
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

st.title(config['appName'])
st.write(config['appDescription'])

# Connect to Google Sheets
gc = gspread.service_account(
    filename=config['GoogleSheets']['credentials']['path'])

# Open the Google Sheet
sh = gc.open(config['GoogleSheets']['spreadsheetName'])

# Get the worksheet
ws_cuentas = sh.worksheet("CUENTAS_TOTALES")

st.write(ws_cuentas.acell("B2").value)

left_column, right_column = st.columns(2)
INGRESOS = left_column.slider("Earnings", 0.0, 4000.0, 2600.0)
YEAR = right_column.slider("YEAR", 2020, 2100, 2024)
MONTH = left_column.slider("MONTH", 1, 12, 7)

# Cargar el pipeline desde el archivo

model = joblib.load("../models/linearregression.joblib")
df = pd.DataFrame(
    data=[[INGRESOS, YEAR, MONTH]],
    columns=['INGRESOS','YEAR','MONTH'],
)
result = model.predict(df)

st.write(f"The estimated spends are: {round(result[0][0], 2)}")
######################
