import yaml
import argparse
import numpy as np
import pandas as pd

def read_params(config_path):
    """
    read parameters from params.yaml file
    input: params.yaml location
    output: paramters as dictionary
    """

    with open(cionfig_path) as yaml_file:
        config=yaml.safe_load(yaml_file)
    return config

def load_data(data_path,selected_featues):
    """
    load csv data from given path
    input: csv path
    output: pandas dataframe with only selected features from config file based on prototype code knowledge.   
    """
    df=pd.read_csv(data_path,sep=",",encoding='utf-8')
    df=df[selected_featues]
    return df

def load_raw_data(config_path):
    """
    load data from location(data/external) to (data/raw) location
    input: config_path
    output: saves the file to data/raw folder
    """
    config=read_params(config_path)
    
    external_data_path=config["external_data_config"]["external_data_csv"]
    raw_data_path=config["raw_data_config"]["raw_data_csv"]
    # selected features
    selected_feat=config["raw_data_config"]["model_var"]
    # load data 
    df=load_data(external_data_path,selected_feat)
    df.to_csv(raw_data_path,index=False)

if __name__='__main__':
    args = argparse.Argumentparser()
    args.add_argument("--config",default="params.yaml")
    parsed_args=args.parse_args()
    load_raw_data(config_path=parsed_args.config)








