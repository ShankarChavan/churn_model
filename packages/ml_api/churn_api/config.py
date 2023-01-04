import os
import pathlib

import pandas as pd


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / 'model_service_dir'

# variables
FEATURES = ['number_vmail_messages','total_day_calls','total_eve_minutes',
            'total_eve_charge','total_intl_minutes','number_customer_service_calls']

# model
MODEL ='model.pkl'

