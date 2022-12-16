import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import streamlit_pydantic as sp
from utils import load_model
from datamodel import churnModelFeilds

def predict_churn(data):
    
    # Extract data in correct order
    clf,features=load_model()
    data_dict = data.dict()
    to_predict = [data_dict[feature] for feature in features]
    to_predict=np.array(to_predict).reshape(1, -1)
    prediction = clf.predict(to_predict)
    return {'prediction':prediction[0]}

st.header("Churn model prediction Engine")

data = sp.pydantic_form(key="churn_predict_form", model=churnModelFeilds,submit_label='predict_churn')

if data:
    prediction=predict_churn(data)
    st.json(data.json())
    st.write(prediction)