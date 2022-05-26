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
        <head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>PSA Project</title>
		<style type="text/css">
			html, #page { padding:0; margin:0;}
			body { margin:0; padding:0; width:100%; color:#787878; font:normal 15px/2.0em Sans-Serif;} 
			h1, h2, h3, h4, h5, h6 {color:darkgreen;}
			#page { background:#fff;}
			#header, #footer, #top-nav, #content, #content #contentbar, #content #sidebar { margin:0; padding:0;text-align:justify;}
						
			/* Logo */
			#logo { padding:0; width:auto; float:left;}
			#logo h1 a, h1 a:hover { color:darkgreen; text-decoration:none;}
			#logo h1 span { color:#BCCE98;}

			/* Header */
			#header { background:#fff; }
			#header-inner { margin:0 auto; padding:0; width:970px; font-size:12px}
			
			/* Feature */
			.feature { background:green;padding:8px;}
			.feature-inner { margin:auto;width:970px;}
			.feature-inner h1 {color:#DAE9BC;font-size:32px;}
			
			/* Menu */
			#top-nav { margin:0 auto; padding:0px 0 0; height:37px; float:right;}
			#top-nav ul { list-style:none; padding:0; height:37px; float:left;}
			#top-nav ul li { margin:0; padding:0 0 0 8px; float:left;}
			#top-nav ul li a { display:block; margin:0; padding:8px 20px; color:green; text-decoration:none;}
			#top-nav ul li.active a, #top-nav ul li a:hover { color:#BCCE98;background-color: #BCCE98; color: #BCCE98}
			
			/* Content */
			#content-inner { margin:0 auto; padding:10px 0; width:970px;background:#fff;}
			#content #contentbar { margin:0; padding:0; float:right; width:760px;}
			#content #contentbar .article { margin:0 0 24px; padding:0 20px 0 15px; }
			#content #sidebar { padding:0; float:left; width:200px;}
			#content #sidebar .widget { margin:0 0 12px; padding:8px 8px 8px 13px;line-height:1.4em;}
			#content #sidebar .widget h3 a { text-decoration:none;}
			#content #sidebar .widget ul { margin:0; padding:0; list-style:none; color:#959595;}
			#content #sidebar .widget ul li { margin:0;}
			#content #sidebar .widget ul li { padding:4px 0; width:185px;}
			#content #sidebar .widget ul li a { color:green; text-decoration:none; margin-left:0px; padding:4px 8px 4px 16px;}
			#content #sidebar .widget ul li a:hover { color:#BCCE98; font-weight:bold; text-decoration:none;}
			
			/* Footerblurb */
			#footerblurb { background:#DAE9BC;color:green;}
			#footerblurb-inner { margin:0 auto; width:922px; padding:24px;}
			#footerblurb .column { margin:0; text-align:justify; float:left;width:250px;padding:0 24px;}
			
			/* Footer */
			#footer { background:#fff;}
			#footer-inner { margin:auto; text-align:center; padding:12px; width:922px;}
			#footer a {color:green;text-decoration:none;}
			
			/* Clear both sides to assist with div alignment  */
			.clr { clear:both; padding:0; margin:0; width:100%; font-size:0px; line-height:0px;}
		</style>
	</head>
	<body>
		<div id="page">
			<header id="header">
				<div id="header-inner">	
					<div id="logo">
						<h1><a>PSA Project<span> &#124; Machine Learning</span></a></h1>
					</div>
					<div class="clr"></div>
				</div>
			</header>
			<div class="feature">
				<div class="feature-inner">
				<h1>Pressure swing adsorption (PSA) unit </h1>
				</div>
			</div>
		
	
			<div id="content">
				<div id="content-inner">
				
					<main id="contentbar">
						<div class="article">
							<p>We'll be looking at the efficiency of Nitrogen (N<sub>2</sub>) separation from a CH<sub>4</sub>-N<sub>2</sub> feed stream by a solid-bed column. Twelve parameters were monitored in order to determine their influence on N<sub>2</sub> separation. To use the PSA app go to the Application page by clicking the proper button in the IMPORTANT MATERIAL or by going to https://psa-unit.herokuapp.com/docs. After that, expand the POST/predict menu, click the "Try it out" button, adjust the input parameters and execute.</p>
                            <h3 style="color: #2e6c80;"><span style="color: darkgreen;">PSA parameters (input):</span></h3>
            <table class="editorDemoTable" style="height: 211px; width: 654px;" border="1px">
            <thead>
            <tr style="height: 18px;">
            <td style="height: 18px; width: 294.438px;text-align: center;"><strong>Name of the parameter</strong></td>
            <td style="height: 18px; width: 245.375px;text-align: center;"><strong>Variable name in the code and&nbsp; in the Heroku's .json input&nbsp;</strong></td>
            <td style="height: 18px; width: 92.1875px;text-align: center;"><strong>Default value</strong></td>
            </tr>
            </thead>
            <tbody>
            <tr style="height: 22px;">
            <td style="height: 10px; width: 294.438px;">Adsorption pressure (bar)</td>
            <td style="width: 245.375px; height: 10px;">Adsorp_pres</td>
            <td class="xl65" style="height: 10px; width: 92.1875px;" height="20">4.8</td>
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
            <h3 style="color: #2e6c80;"><span style="color: darkgreen;">PSA parameter (output):</span></h3>
            <table class="editorDemoTable" style="width: 654px;" border="1px">
            <thead>
            <tr style="height: 18px;">
            <td style="height: 18px; width: 285.5px;text-align: center;"><strong>Name of the parameter</strong></td>
            <td style="height: 18px; width: 352.5px;text-align: center;"><strong>Variable name in the code</strong></td>
            </tr>
            </thead>
            <tbody>
            <tr style="height: 22px;">
            <td style="height: 10px; width: 285.5px;">N<sub>2</sub> mole fraction in the purified stream</td>
            <td style="width: 352.5px;">PurStream_N2_mf</td>
            </tr>
            </tbody>
            </table>
						</div>
					</main>
					
					<nav id="sidebar">
						<div class="widget">
							<h3>IMPORTANT MATERIAL</h3>
							<ul>
                              <li><a style="background-color: #009d00; color: #f2f8e8; display: inline-block; padding: 3px 10px; font-weight: bold; border-radius: 4px;" title="https://www.sciencedirect.com/science/article/pii/S0098135417302053" href="https://www.sciencedirect.com/science/article/pii/S0098135417302053">Database</a></li>
                              
                            <li><a style="background-color: #009d00; color: #f2f8e8; display: inline-block; padding: 3px 10px; font-weight: bold; border-radius: 4px;" title="https://psa-unit.herokuapp.com/docs" href="https://psa-unit.herokuapp.com/docs">Application page</a></li>
                            
                            <li><a style="background-color: #009d00; color: #f2f8e8; display: inline-block; padding: 3px 10px; font-weight: bold; border-radius: 4px;" title="https://github.com/nupeg/PSAUnit_MachileLearning" href="https://github.com/nupeg/PSAUnit_MachileLearning">Github repository</a></li>
							</ul>
						</div>
					</nav>
					
					<div class="clr"></div>
				</div>
			</div>
		
			<div id="footerblurb">
				<div id="footerblurb-inner">
				
					<div>
						<h2><span>Additional information</span></h2>
						<p>Designed and implemented by <a href="https://orcid.org/0000-0002-7980-1040">Mário H. Moura-Neto</a> and <a href="https://orcid.org/0000-0002-7243-5463">Mateus F. Monteiro</a>. <br> For more detailed material on the project's conceptualization and execution please read the README.md file in the github repository.</p>
					</div>	
					</div>	
					
					<div class="clr"></div>
				</div>
			</div>
			<footer id="footer">
				<div id="footer-inner">
					<p>&copy; Copyright 2022 - All Rights Reserved - <a href="https://github.com/nupeg/PSAUnit_MachileLearning"> Legal</a></p>
					<div class="clr"></div>
				</div>
			</footer>
	</body>
    """

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