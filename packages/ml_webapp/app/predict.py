import argparse
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from utils import load_model
from validation import validate_inputs


def predict_churn(data):
    
    # Extract data in correct order
    clf,features=load_model()
    prediction = clf.predict(data.values)
    return pd.DataFrame(prediction).rename(columns={0:'predictions'})

def make_prediction(input_data:pd.DataFrame):
    """
    input_data pd.DataFrame: input data
    output: prediction output 
    """
    data=input_data    
    validated_data=validate_inputs(data)
    output=predict_churn(validated_data)
    return output
