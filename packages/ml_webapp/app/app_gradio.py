
import gradio as gr
import pandas as pd
from utils import load_sample_data
from predict import make_prediction

def predict_churn(data):
    prediction=make_prediction(data)
    return prediction


def load_data():
    return load_sample_data()


# title and description are optional
title = "Churn Prediction"

inputs = [gr.Dataframe(row_count = (10, "dynamic"), col_count=(6,"dynamic"), label="Input Data", interactive=0)]

outputs = [gr.Dataframe(row_count = (10, "dynamic"), col_count=(1, "fixed"), label="Output", headers=["Churn"])]

#load sample df 
df=load_data()

# create front-end interface  
demo=gr.Interface(fn = predict_churn, inputs = inputs, outputs = outputs, examples = [df.head(10)])

if __name__=='__main__':
    demo.launch(auth=("admin","admin"),show_error=True,server_name="0.0.0.0", server_port=8080)