######################
#     LIBRARIES      #
######################
import ast
import streamlit as st
import sys
import gspread
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
######################
