"""
This script is used to start the Streamlit app.
It reads the configuration file, sets the logging and starts the Streamlit app.
"""

######################
#     LIBRARIES      #
######################
import logging
import os
import subprocess

from datetime import datetime
from utils.utils import read_config
######################

######################
#     FUNCTIONS      #
######################
def start_streamlit_app(script_path, config):
    """
    Start Streamlit app.
    """

    try:
        subprocess.run(["streamlit", "run", script_path, f"{config}"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error("Error when starting Streamlit app: %s", e)
######################

######################
#        MAIN        #
######################

# Read config file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config/my-wallet-manager.yml")
    )
config = read_config(config_path)

# Creamos el directorio de logs si no existe
logs_dir = os.path.join(os.path.dirname(__file__), config['logs']['path'])
os.makedirs(logs_dir, exist_ok=True)

# Set logging
logging.basicConfig(filename=f'{logs_dir}/{datetime.now().date().strftime("%Y_%m_%d")}.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

# Start Streamlit app
if config:
    #if os.path.exists(f"src/{config['scriptName']}.py"):
    if os.path.exists(
        os.path.join(os.path.dirname(__file__), f"{config['scriptName']}.py")
        ):
        start_streamlit_app(
            os.path.join(os.path.dirname(__file__), f"{config['scriptName']}.py"), str(config)
            )
    else:
        logging.error("Error when starting Streamlit app: %s.py does not exist.\
                      Please reviw configuration file.", config['scriptName'])
######################
