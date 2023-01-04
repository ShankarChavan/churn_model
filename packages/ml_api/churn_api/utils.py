import pickle
import os 
import config

def load_model():
    """
    load the model and features
    """
    model_path=os.path.join(config.TRAINED_MODEL_DIR,config.MODEL)
    with open(model_path,'rb') as modelfile:
        model=pickle.load(modelfile)
    features=config.FEATURES
    return model,features