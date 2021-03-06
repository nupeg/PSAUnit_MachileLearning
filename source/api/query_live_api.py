"""
Creator: Ivanovitch Silva
Date: 26 April. 2022
Script that POSTS to the API using the requests 
module and returns both the result of 
model inference and the status code
"""
import requests
import json
import pprint

conditions = {
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

#url = "http://127.0.0.1:8000"
url = "https://n2-purity-app.herokuapp.com/"
response = requests.post(f"{url}/predict",
                         json=conditions)

print(f"Request: {url}/predict")
print("-- CONDITIONS -- \n"\
      f"Adsorp_pres: {conditions['Adsorp_pres']}\n"\
      f"CoCur_BlowPres: {conditions['CoCur_BlowPres']}\n"\
      f"CountCur_pres: {conditions['CountCur_pres']}\n"\
      f"Adsorp_time: {conditions['Adsorp_time']}\n"\
      f"CoCur_desorp_time: {conditions['CoCur_desorp_time']}\n"\
      f"CountCur_desorp_time: {conditions['CountCur_desorp_time']}\n"\
      f"Compres_time: {conditions['Compres_time']}\n"\
      f"Vol_flow: {conditions['Vol_flow']}\n"\
      f"Temp: {conditions['Temp']}\n"\
      f"Col_length: {conditions['Col_length']}\n"\
      f"Col_diam: {conditions['Col_diam']}\n"\
      f"Temp: {conditions['Temp']}\n"\
      f"Feed_N2_mf: {conditions['Feed_N2_mf']}\n"
     )
print(f"Result of model inference: {response.json()}")
print(f"Status code: {response.status_code}")