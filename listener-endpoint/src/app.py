import time
import os
from datetime import datetime
import logging

def main():
    # Creamos el directorio de logs si no existe
    logs_dir = '../logs'
    os.makedirs(logs_dir, exist_ok=True)

    # Set logging
    logging.basicConfig(filename=f'{logs_dir}/{datetime.now().date().strftime("%Y_%m_%d")}.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w')
    while True:
        # Aquí colocarías la lógica para escuchar continuamente y hacer peticiones a la API de Yahoo Finance
        logging.info(f"Escuchando y haciendo peticiones.")
        time.sleep(5)  # Ejemplo: espera 5 segundos antes de la próxima petición
        logging.info(f"Una peticion")

if __name__ == "__main__":
    main()
