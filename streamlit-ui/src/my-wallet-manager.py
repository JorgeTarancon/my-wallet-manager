######################
#     LIBRARIES      #
######################
import ast
import streamlit as st
import sys
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
######################
