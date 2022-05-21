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
        <h1 style="color: #5e9ca0;"><span style="text-decoration: underline; color: #000080;">Pressure swing adsorption (PSA) unit&nbsp;</span></h1>
        <p style="text-align: justify;">We'll be looking at the efficiency of Nitrogen (N<sub>2</sub>) separation from a CH<sub>4</sub>-N<sub>2</sub> feed stream by a distillation column. Twelve parameters were monitored in order to determine their influence on N<sub>2</sub> separation.</p>
        <ul>
        <li style="text-align: justify;">The used <span style="text-decoration: underline;">database</span> can be found by clicking on the following text:&nbsp;<strong><span style="color: #ffffff; background-color: #000080; padding: 0.5px 3px;"><a style="color: #ffffff; background-color: #000080;" title="Machine learning model and optimization of a PSA unit for methane-nitrogen separation" href="Machine learning model and optimization of a PSA unit for methane-nitrogen separation">See paper</a></span></strong>.</li>
        <li>To go to the <span style="text-decoration: underline;">application</span> execution page click <span style="background-color: #008000; color: #ffffff;"><strong><a style="background-color: #008000; color: #ffffff;" title="https://n2-purity-app.herokuapp.com/docs" href="https://n2-purity-app.herokuapp.com/docs">here</a></strong></span>.</li>
        <li>To go to the <span style="text-decoration: underline;">Github</span> repository click <span style="color: #ffffff; background-color: #333333;"><strong><a style="color: #ffffff; background-color: #333333;" title="https://github.com/nupeg/PSAUnit_MachileLearning" href="https://github.com/nupeg/PSAUnit_MachileLearning">here</a></strong></span>.</li>
        </ul>
        <h3 style="color: #2e6c80;"><span style="color: #000080;">PSA parameters (input):</span></h3>
        <table class="editorDemoTable" style="height: 211px; width: 654px;">
        <thead>
        <tr style="height: 18px;">
        <td style="height: 18px; width: 294.438px; text-align: center;"><strong>Name of the parameter</strong></td>
        <td style="height: 18px; width: 245.375px; text-align: center;"><strong>Variable name in the code and&nbsp; in the Heroku's .json input&nbsp;</strong></td>
        <td style="height: 18px; width: 92.1875px; text-align: center;"><strong>Default value</strong></td>
        </tr>
        </thead>
        <tbody>
        <tr style="height: 22px;">
        <td style="height: 10px; width: 294.438px;">Adsorption pressure (bar)</td>
        <td style="width: 245.375px; height: 10px;">Adsorp_pres</td>
        <td class="xl65" style="height: 10px; width: 92.1875px;" height="20">5.2</td>
        </tr>
        <tr style="height: 36px;">
        <td style="width: 294.438px; height: 10px;">Co-current blowdown pressure (bar)</td>
        <td style="width: 245.375px; height: 10px;">CoCur_BlowPres</td>
        <td class="xl65" style="height: 10px; width: 92.1875px;" height="20">4.5</td>
        </tr>
        <tr style="height: 36px;">
        <td style="width: 294.438px; height: 10px;">Counter-current blowdown pressure (bar)</td>
        <td style="width: 245.375px; height: 10px;">CountCur_pres</td>
        <td class="xl65" style="height: 10px; width: 92.1875px;" height="20">0.13</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Adsorption time (s)</td>
        <td style="width: 245.375px; height: 18px;">Adsorp_time</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">53.5</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Co-current desorption time (s)</td>
        <td style="width: 245.375px; height: 18px;">CoCur_desorp_time</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">30.5</td>
        </tr>
        <tr style="height: 36px;">
        <td style="width: 294.438px; height: 19px;">Counter-current desorption time (s)</td>
        <td style="width: 245.375px; height: 19px;">CountCur_desorp_time</td>
        <td class="xl65" style="height: 19px; width: 92.1875px;" height="20">33</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Compression time (s)</td>
        <td style="width: 245.375px; height: 18px;">Compres_time</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">21.9</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Volumetric flow (m<sup>3</sup>&middot;s<sup>-1</sup>)</td>
        <td style="width: 245.375px; height: 18px;">Vol_flow</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">0.001</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Temperature (K)</td>
        <td style="width: 245.375px; height: 18px;">Temp</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">296.3</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Column length (m)</td>
        <td style="width: 245.375px; height: 18px;">Col_length</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">1.3</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Column diameter (m)</td>
        <td style="width: 245.375px; height: 18px;">Col_diam</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">0.26</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 294.438px; height: 18px;">Feed nitrogen mole fraction</td>
        <td style="width: 245.375px; height: 18px;">Feed_N2_mf</td>
        <td class="xl65" style="height: 18px; width: 92.1875px;" height="20">0.76</td>
        </tr>
        </tbody>
        </table>
        <h3 style="color: #2e6c80;">&nbsp;</h3>
        <h3 style="color: #2e6c80;"><span style="color: #000080;">PSA parameter (output):</span></h3>
        <table class="editorDemoTable" style="width: 654px;">
        <thead>
        <tr style="height: 18px;">
        <td style="height: 18px; width: 285.5px; text-align: center;"><strong>Name of the parameter</strong></td>
        <td style="height: 18px; width: 352.5px; text-align: center;"><strong>Variable name in the code</strong></td>
        </tr>
        </thead>
        <tbody>
        <tr style="height: 22px;">
        <td style="height: 10px; width: 285.5px;">N<sub>2</sub> mole fraction in the purified stream</td>
        <td style="width: 352.5px;">PurStream_N2_mf</td>
        </tr>
        </tbody>
        </table>
    """
        
    #return """
    #<p><span style="font-size:28px"><strong>Hello World</strong></span></p>"""\
    #"""<p><span style="font-size:20px">In this project, we will apply the skills """\
    #    """acquired in the Deploying a Scalable ML Pipeline in Production course to develop """\
    #    """ a regression model on Pressure swing adsorption (PSA): efficiency of N2 separation from a CH4-N2 feed stream by a distillation column. Twelve #    #    parameters were monitored in order to determine their influence on N2 separation"""\
    #    """<a href="https://doi.org/10.1016/j.compchemeng.2017.05.006"> Column data from this paper</a>.</span></p>"""

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