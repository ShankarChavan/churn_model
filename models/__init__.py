import joblib

def load_model():
    model=joblib.load('models/model.joblib')
    return model

    
