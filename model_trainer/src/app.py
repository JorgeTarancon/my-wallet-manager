"""
Model Trainer Script

This script is used to train the model.
"""

######################
#     LIBRARIES      #
######################
import os
import logging
from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

from utils.utils import read_config, read_gsheet, get_env_variable
######################


######################
#     FUNCTIONS      #
######################
def evaluate(y_test, y_pred) -> tuple:
    """
    Regression evaluation.
    """

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"\tMean Squared Error (MSE): {mse}")
    print(f"\tRoot Mean Squared Error (RMSE): {rmse}")
    print(f"\tR-squared (R2) Score: {r2}")

    #return mse, rmse, r2

def split_train_test(df: pd.DataFrame, features: list,
                     target: list, test_size:float=0.2,
                     random_state:int=42) -> tuple:
    """
    Train test split function.
    """

    x, y = df[features], df[target]

    # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size,
                                                        random_state=random_state)

    print(f"Number of training instances: {len(x_train)}")
    print(f"Number of testing instances: {len(x_test)}")

    return x_train, x_test, y_train, y_test

def create_pipeline(model: object) -> object:
    """
    Create a ml pipeline.
    """

    pipeline = Pipeline([
        ('scaler', StandardScaler()), # Standardize features
        ('regressor', model) # Regressor model
    ])

    return pipeline

def ml_pipeline(x_train, y_train, x_test, y_test, *args) -> None:
    """
    Creates as many ml pipelines as *args.
    """

    for arg in args:
        print(f'---{arg.steps[1][1].__class__.__name__}---')
        # Fit the pipeline on the training data
        arg.fit(x_train, y_train)
        # Predict on the test set
        y_pred = arg.predict(x_test)

        evaluate(y_test, y_pred)

def save_models(*args) -> None:
    """
    Save models into joblib file.
    """

    for arg in args:
        print(f"Saving {arg.steps[1][1].__class__.__name__} model...")
        joblib.dump(arg, f"../models/{arg.steps[1][1].__class__.__name__.lower()}.joblib")

def main(app_config: dict):
    """
    Función principal.
    """

    # Creamos el directorio de logs si no existe
    logs_dir = os.path.join(os.path.dirname(__file__), app_config['logs']['path'])
    os.makedirs(logs_dir, exist_ok=True)

    # Set logging
    logging.basicConfig(
        filename=f'{logs_dir}/{datetime.now().date().strftime("%Y_%m_%d")}.log',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="w",
    )

    gs_credentials = get_env_variable(variable="GOOGLE_SHEETS_CREDENTIALS",
                                        is_json=True)

    ws_contabilidad = read_gsheet(gc_credentials=gs_credentials,
                                    spreadsheet_name="Mock_Cartera_de_acciones",
                                    worksheet_name="CONTABILIDAD")
    # Build a dataframe from the worksheet
    data = ws_contabilidad.get_all_values()
    df = pd.DataFrame(data=data[1:],columns=data[0])
    print(df.head())

    # PREPROCESS. WIP -> ABSTRACT INTO FUNCTIONS
    month_numbers = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
    'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    df['MONTH'] = df['FECHA'].map(lambda x: x.split('-')[0]).map(month_numbers)
    df['YEAR'] = df['FECHA'].map(lambda x: int(x.split('-')[1]))

    df.drop(columns=['FECHA', 'OBSERVACIONES', 'PORCENTAJE LIQUIDEZ',
                     'PORCENTAJE INVERSIÓN', 'PORCENTAJE GASTOS'],
            inplace=True)

    df['INGRESOS'] = df['INGRESOS'].map(lambda x: x.replace('€', '').strip().\
                                    replace('.','').replace(',','.')).\
                                    astype(float)
    df['GASTOS'] = df['GASTOS'].map(lambda x: x.replace('€', '').strip().\
                                    replace('.','').replace(',','.')).\
                                    astype(float)
    df['INVERSIÓN'] = df['INVERSIÓN'].map(lambda x: x.replace('€', '').strip().\
                                    replace('.','').replace(',','.')).\
                                    astype(float)
    df['LIQUIDEZ'] = df['LIQUIDEZ'].map(lambda x: x.replace('€', '').strip().\
                                    replace('.','').replace(',','.')).\
                                    astype(float)

    # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = split_train_test(df=df,
                                                        features=['INGRESOS','YEAR','MONTH'],
                                                        target=['GASTOS'])

    # Create pipelines
    lr_pipeline = create_pipeline(model=LinearRegression()) # Linear regression pipeline
    xgboost_pipeline = create_pipeline(model=XGBRegressor(n_estimators=1000)) # XGBoost pipeline

    # Run pipelines
    ml_pipeline(x_train, y_train, x_test, y_test, lr_pipeline, xgboost_pipeline)

    # Save models
    save_models(lr_pipeline, xgboost_pipeline)

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
