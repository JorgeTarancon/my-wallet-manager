######################
#     LIBRARIES      #
######################
import ast
import streamlit as st
import sys
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

st.title(config['appName'])
st.write(config['appDescription'])

ws_cuentas = read_gsheet(gc_credentials=config['GoogleSheets']['credentials']['path'],
                         spreadsheet_name=config['GoogleSheets']['spreadsheetName'],
                         worksheet_name="CUENTAS_TOTALES")

st.write(ws_cuentas.acell("B2").value)

left_column, right_column = st.columns(2)
INGRESOS = left_column.slider("Earnings", 0.0, 4000.0, 2600.0)
YEAR = right_column.slider("YEAR", 2020, 2100, 2024)
MONTH = left_column.slider("MONTH", 1, 12, 7)

# Load model from models folder
model = joblib.load(f"{config['Models']['path']}/linearregression.joblib")
df = pd.DataFrame(
    data=[[INGRESOS, YEAR, MONTH]],
    columns=['INGRESOS','YEAR','MONTH'],
)
result = model.predict(df)

st.write(f"The estimated spends are: {round(result[0][0], 2)}")
######################
