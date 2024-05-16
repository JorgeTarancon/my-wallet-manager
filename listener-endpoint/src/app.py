"""
Listener Endpoint Script

This script is used as a listentener and making requests to the Yahoo Finance API.
"""

######################
#     LIBRARIES      #
######################
import time
import os
from datetime import datetime
import logging

from utils.utils import read_config
######################


######################
#     FUNCTIONS      #
######################
def main(config: dict):
    """
    Función principal.
    """

    # Creamos el directorio de logs si no existe
    logs_dir = os.path.join(os.path.dirname(__file__), config['logs']['path'])
    os.makedirs(logs_dir, exist_ok=True)

    # Set logging
    logging.basicConfig(
        filename=f'{logs_dir}/{datetime.now().date().strftime("%Y_%m_%d")}.log',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="w",
    )
    while True:
        # Aquí colocarías la lógica para escuchar continuamente
        # y hacer peticiones a la API de Yahoo Finance
        logging.info("Escuchando y haciendo peticiones.")
        time.sleep(5)  # Ejemplo: espera 5 segundos antes de la próxima petición
        logging.info("Una peticion")


######################

######################
#        MAIN        #
######################

# Read config file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__),"../../config/my-wallet-manager.yml")
    )
config = read_config(config_path)

if __name__ == "__main__":
    main(config)
######################
