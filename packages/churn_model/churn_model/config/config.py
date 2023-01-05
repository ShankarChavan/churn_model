import os
import pathlib

import churn_model

import pandas as pd


pd.options.display.max_rows = 10
pd.options.display.max_columns = 10


PACKAGE_ROOT = pathlib.Path(churn_model.__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'model_dir'
DATASET_DIR = PACKAGE_ROOT / 'datasets'



# data
TESTING_DATA_FILE = 'churn_test.csv'
TARGET = 'churn'


# variables
FEATURES = ['number_vmail_messages','total_day_calls','total_eve_minutes',
            'total_eve_charge','total_intl_minutes','number_customer_service_calls']

# model
MODEL ='model.pkl'

