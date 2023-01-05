import os
import pickle
import config
import pandas as pd


def load_model():
    model_path=os.path.join(config.TRAINED_MODEL_DIR,config.MODEL)
    with open(model_path,'rb') as modelfile:
        model=pickle.load(modelfile)
    
    features=config.FEATURES
    return model,features

def load_sample_data():
    df=pd.read_csv(os.path.join(config.DATASET_DIR,config.TESTING_DATA_FILE))
    return df