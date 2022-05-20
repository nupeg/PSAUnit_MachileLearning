"""
Creator: Ivanovitch Silva
Date: 18 April 2022
API testing
"""
from fastapi.testclient import TestClient
import os
import sys
import pathlib
from source.api.main import app

# Instantiate the testing client with our app.
client = TestClient(app)

# a unit test that tests the status code of the root path
def test_root():
    r = client.get("/")
    assert r.status_code == 200

# a unit test that tests the status code and response 
# for an instance with a low income
def test_get_PSA_N2Purity():

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

    r = client.post("/predict", json=conditions)
    # print(r.json())
    assert r.status_code == 200
    #assert r.json() > 0.8