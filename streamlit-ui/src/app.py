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
    try:
        subprocess.run(["streamlit", "run", script_path, f"{config}"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error when starting Streamlit app: {e}")
######################

######################
#        MAIN        #
######################

# Read config file
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/my-wallet-manager.yml"))
config = read_config(config_path)

# Creamos el directorio de logs si no existe
logs_dir = config['logs']['path']
os.makedirs(logs_dir, exist_ok=True)

# Set logging
logging.basicConfig(filename=f'{logs_dir}/{datetime.now().date().strftime("%Y_%m_%d")}.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

# Start Streamlit app
if config:
    if os.path.exists(f"src/{config['scriptName']}.py"):
        start_streamlit_app(f"src/{config['scriptName']}.py", str(config))
    else:
        logging.error(f"Error when starting Streamlit app: {config['scriptName']}.py does not exist. Please reviw configuration file.")
######################
