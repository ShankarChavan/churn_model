import yaml
import os
import joblib

def read_params(config_path='webapp_params.yaml'):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    #cwd=os.getcwd()
    cwd= os.path.dirname(os.path.realpath(__file__))
    with open(cwd+'/'+config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def load_model(config_path="webapp_params.yaml"):
    config=read_params(config_path)
    model=joblib.load(config["model_dir"])
    features=config["model_var"]
    return model,features
