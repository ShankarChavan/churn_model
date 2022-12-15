import joblib
import argparse
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.ensemble import RandomForestClassifier

from utils import read_params
from datamodel import churnModelFeilds

#Instance of FastAPI class
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def load_model(config_path="service_params.yaml"):
    config=read_params(config_path)
    model=joblib.load(config["model_dir"])
    features=config["model_var"]
    return model,features

@app.get('/')
async def index():
    return {'healthcheck':'True'}

@app.post("/predict")
def predict_churn(data: churnModelFeilds):
    
    # Extract data in correct order
    clf,features=load_model()
    data_dict = data.dict()
    to_predict = [data_dict[feature] for feature in features]
    to_predict=np.array(to_predict).reshape(1, -1)
    prediction = clf.predict(to_predict)
    return {"prediction": prediction[0]}

