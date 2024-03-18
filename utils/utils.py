######################
#     LIBRARIES      #
######################
import os
import yaml
import logging
######################

######################
#     FUNCTIONS      #
######################
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            logging.error(f"Error reading the file: {file_path} - {e}")

def read_config(file_path):
    if os.path.exists(file_path):
        return read_yaml(file_path)
    else:
        logging.error(f"Error reading the file: {file_path} - File not found.")
        return None
######################
