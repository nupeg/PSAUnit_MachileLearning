"""
Creator: Ivanovitch Silva
Date: 17 April 2022
Create API
"""
# from typing import Union
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
import pandas as pd
import joblib
import os
import wandb
import sys
from source.api.pipeline import NumericalTransformer #FeatureSelector, CategoricalTransformer,

# global variables
#setattr(sys.modules["__main__"], "FeatureSelector", FeatureSelector)
#setattr(sys.modules["__main__"], "CategoricalTransformer", CategoricalTransformer)
setattr(sys.modules["__main__"], "NumericalTransformer", NumericalTransformer)

# name of the model artifact
artifact_model_name = "psa_dec_tree_reg_v1/model_export:latest"

# initiate the wandb project
run = wandb.init(project="psa_dec_tree_reg_v1",job_type="api")

# create the api
app = FastAPI()

# declare request example data using pydantic
# a person in our dataset has the following attributes
class Conditions(BaseModel):
    Adsorp_pres: float
    CoCur_BlowPres: float
    CountCur_pres: float
    Adsorp_time: float
    CoCur_desorp_time: float
    CountCur_desorp_time: float
    Compres_time: float
    Vol_flow: float
    Temp: float
    Col_length: float
    Col_diam: float
    Feed_N2_mf: float

    class Config:
        schema_extra = {
            "example": {
                'Adsorp_pres':4.8,
                'CoCur_BlowPres':4.5,
                'CountCur_pres':0.13,
                'Adsorp_time':51.5,
                'CoCur_desorp_time':30.5,
                'CountCur_desorp_time':40,
                'Compres_time':21.9,
                'Vol_flow':0.0015,
                'Temp':296.9,
                'Col_length':1.5,
                'Col_diam':0.28,
                'Feed_N2_mf':0.76
            }
        }

# give a greeting using GET
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <p><span style="font-size:28px"><strong>Hello World</strong></span></p>"""\
    """<p><span style="font-size:20px">In this project, we will apply the skills """\
        """acquired in the Deploying a Scalable ML Pipeline in Production course to develop """\
        """ a regression model on Pressure swing adsorption (PSA): efficiency of N2 separation from a CH4-N2 feed stream by a distillation column. Twelve parameters were monitored in order to determine their influence on N2 separation"""\
        """<a href="https://doi.org/10.1016/j.compchemeng.2017.05.006"> Column fata from this paper</a>.</span></p>"""

# run the model inference and use a Person data structure via POST to the API.
@app.post("/predict")
async def get_inference(conditions: Conditions):
    
    #IMPLEMENTAR O TESTE EM TODAS AS VARIAVEIS PARA CHECAR SE ESTAO NOS LIMITES. COLOCAR IF E MOSTRAR MENSAGEM DE ERRO CASO ALGUMA NAO ESTEJA
    
    # Download inference artifact
    model_export_path = run.use_artifact(artifact_model_name).file()
    pipe = joblib.load(model_export_path)
    
    # Create a dataframe from the input feature
    # note that we could use pd.DataFrame.from_dict
    # but due be only one instance, it would be necessary to
    # pass the Index.
    df = pd.DataFrame([conditions.dict()])

    # Predict test data
    predict = pipe.predict(df)
    #print(f"N2 mole fraction in the purified stream: {predict[0]}")
    
    return predict[0]