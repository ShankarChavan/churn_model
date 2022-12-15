import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import streamlit_pydantic as sp
from utils import read_params
from datamodel import churnModelFeilds




def load_model(config_path="webapp_params.yaml"):
    config=read_params(config_path)
    model=joblib.load(config["model_dir"])
    features=config["model_var"]
    return model,features

def predict_churn(data):
    
    # Extract data in correct order
    clf,features=load_model()
    data_dict = data.dict()
    to_predict = [data_dict[feature] for feature in features]
    to_predict=np.array(to_predict).reshape(1, -1)
    prediction = clf.predict(to_predict)
    return {'prediction':prediction[0]}

st.write("# Churn model prediction Engine for telecom company -Yoda")

data = sp.pydantic_form(key="churn_predict_form", model=churnModelFeilds,submit_label='predict_churn')

if data:
    prediction=predict_churn(data)
    st.json(data.json())
    st.write(prediction)