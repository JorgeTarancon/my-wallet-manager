"""
This module contains utility functions that are used in the project.
"""

######################
#     LIBRARIES      #
######################
import os
import logging
import json
import yaml
import gspread
from dotenv import load_dotenv
######################

######################
#     FUNCTIONS      #
######################
def read_yaml(file_path):
    """
    Read a YAML file.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            logging.error("Error reading the file: %s - %s", file_path, e)
            return None

def read_config(file_path):
    """
    Read a YAML file with the configuration.
    """

    if os.path.exists(file_path):
        return read_yaml(file_path)
    logging.error("Error reading the file: %s - File not found.", file_path)
    return None

def read_gsheet(gc_credentials: str = None,
                spreadsheet_name: str = None,
                worksheet_name: str = None):
    """
    Read a Google Sheet.
    """

    # Connect to Google Sheets
    gc = gspread.service_account_from_dict(
        gc_credentials)

    # Open the Google Sheet
    sh = gc.open(spreadsheet_name)

    # Get the worksheet
    gsheet = sh.worksheet(worksheet_name)

    return gsheet

def get_env_variable(env_filepath: str,
                    variable: str = None,
                    is_json: bool = False):
    """
    Read an environment variable.
    """
    try:
        load_dotenv(env_filepath)
    except Exception as e:
        logging.error("Error loading the .env file: %s", e)

    credentials = os.getenv(variable)

    if is_json:
        credentials = json.loads(credentials)

    return credentials
######################
