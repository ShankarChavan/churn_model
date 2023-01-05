import os
import pickle
import pandas as pd
from churn_model.config import config


def load_model():
    """
    load the model 
    """
    model_path=os.path.join(config.TRAINED_MODEL_DIR,config.MODEL)
    with open(model_path,'rb') as modelfile:
        model=pickle.load(modelfile)
    
    features=config.FEATURES
    return model,features

def load_dataset():
    data=pd.read_csv(os.path.join(config.DATASET_DIR,config.TESTING_DATA_FILE))
    return data
