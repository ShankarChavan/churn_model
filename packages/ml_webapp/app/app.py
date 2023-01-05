import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
from pydantic import BaseModel,Field
import streamlit_pydantic as sp
from utils import load_model


class churnModelFeilds(BaseModel):
    """
    Datamodel class for input data with feild Validation.This class will ensure that input data-points are validated for within min-max range values.
    This is important because our model is trained accordingly.  
    """
    number_vmail_messages:float = Field(..., ge=0.0, le=52.0)
    total_day_calls:float= Field(...,ge= 0.0, le= 165.0)
    total_eve_minutes:float= Field(...,ge = 0.0, le= 359.3)
    total_eve_charge:float= Field(...,ge = 0.0, le= 30.54)
    total_intl_minutes:float= Field(...,ge = 0.0, le= 20.0)
    number_customer_service_calls:float= Field(...,ge= 0.0, le= 9.0)
    
    class Config:
        validate_assignment = True


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