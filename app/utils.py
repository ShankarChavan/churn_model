import yaml
import os


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