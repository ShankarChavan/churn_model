import joblib
import argparse
import numpy as np
from pydantic import BaseModel,Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.ensemble import RandomForestClassifier
from src.data.load_data import read_params


class churnModelFeilds(BaseModel):
    """
    Feild Validation class for input data
    """
    number_vmail_messages:float = Field(..., ge=0.0, le=52.0)
    total_day_calls:float= Field(...,ge= 0.0, le= 165.0)
    total_eve_minutes:float= Field(...,ge = 0.0, le= 359.3)
    total_eve_charge:float= Field(...,ge = 0.0, le= 30.54)
    total_intl_minutes:float= Field(...,ge = 0.0, le= 20.0)
    number_customer_service_calls:float= Field(...,ge= 0.0, le= 9.0)
    
    class Config:
        validate_assignment = True
        schema_extra = {
            "example": {
                "number_vmail_messages": 32.0,
                "total_day_calls": 15.0,
                "total_eve_minutes": 20.0,
                "total_eve_charge": 24.0,
                "total_intl_minutes": 3.0,
                "number_customer_service_calls":4.0,
            }
        }


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


def load_model(config_path="../params.yaml"):
    config=read_params(config_path)
    model=joblib.load('../'+config["model_dir"])
    features=config["raw_data_config"]["model_var"]
    return model,features

@app.get('/')
async def index():
    return {'healthcheck':'True'}

@app.post("/predict")
def predict_churn(data: churnModelFeilds):
    
    # Extract data in correct order
    clf,features=load_model()
    data_dict = data.dict()
    to_predict = [data_dict[feature] for feature in features if feature!='churn']
    to_predict=np.array(to_predict).reshape(1, -1)
    prediction = clf.predict(to_predict)
    return {"prediction": prediction[0]}

