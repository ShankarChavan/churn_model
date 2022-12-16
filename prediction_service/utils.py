import yaml
import joblib

def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def load_model(config_path="service_params.yaml"):
    """
    load the model 
    """
    config=read_params(config_path)
    model=joblib.load(config["model_dir"])
    features=config["model_var"]
    return model,features