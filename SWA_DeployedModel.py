# -*- coding: utf-8 -*-
""" Smartworks Analytics - Consuming REST API of a Deployed Model
Author:         C.Chee
Status:    
Last Updated:  

Run:
1. This program can be run directly, i.e. python <filename>
"""
import os.path
import numpy as np
import pandas as pd
import requests
import json
import csv

# CONSTANTS
FILE_PASSWORD = 'password.txt'
FILE_INPUT_DATA = os.path.join('data','data_age_rel.csv')    # relative to this folder

AUTH_URL = "https://artemis.dev-knowledgeworks.altair.com/auth/realms/knowledgeworks/protocol/openid-connect/token"
## Smartworks Artemis constants
DEPLOYMENT_NAME = "cckscensusagerltnshpdeploy"
ML_REQUEST_URL = "https://seldon-qa.dev-knowledgeworks.altair.com/seldon/seldon-artemis/cckscensusagerltnshpdeploy/api/v1.0/predictions".format(DEPLOYMENT_NAME)



def getToken():
    """Getting password separately from external file
    Calls the first REST API for authentication by passing in a string of parameters, including user/password
    :returns token: (str) - the token string retrieve from the REST API       
    """
    with open(FILE_PASSWORD, 'r') as infile:
        for aline in infile:
            mypassword = aline.strip()
    
    swa_cred_json = '{ "username": "cchee",  "password": "' + mypassword + '",  "grant_type": "password",  "client_id": "web-client" }'
    swa_auth_data = json.loads(swa_cred_json) 

    # Requesting token
    swa_resp = requests.post(url=AUTH_URL, data=swa_auth_data)
    token = swa_resp.json()["access_token"]
    return token


def getModelResults(atoken: str, data_head, data_body):
    """Getting the ML scoring results
    Calls the second REST API, by feeding in input data into the ML REST API, and returns the results.
    :param atoken: (str) - the token string obtained from getToken()       
    :return swa_resp: the response object that is obtained by calling the REST API for model prediction scoring.
    """
    #REQUEST_DATA = {"data": {
    #    "ndarray": [[50, "Husband"], [28, "Unmarried"], [32, "Husband"], [28, "Wife"], [32, "Wife"], [28, "Unmarried"]],
    #    "names": ["age", "relationship"]}}

    swa_req_data = {"data": {
        "ndarray": data_body,
        "names": data_head}}

    swa_req_header = {'Authorization': 'Bearer {}'.format(atoken), "Content-Type": "application/json"}

    swa_resp = requests.post(url=ML_REQUEST_URL, data=json.dumps(swa_req_data), headers=swa_req_header)
    print(swa_resp.json())
    return swa_resp

    
def read_input(file01):
    """Reads input data from file
    Calls the second REST API, by feeding in input data into the ML REST API, and returns the results.
    :param file01: (str) - the file to read, which contains data for the ML model scoring
    :return csv_header: (list) - contain the column header names of the input file
    :return csv_data: (list of lists) - the data that was raed from file01
    """
    with open(file01, 'r') as read_obj:
        csv_read = csv.reader(read_obj)
        list_of_rows = list(csv_read)

    csv_header = list_of_rows[0]
    csv_data = list_of_rows[1:]
    return csv_header, csv_data

if __name__ == "__main__":
    input_header, input_data = read_input(FILE_INPUT_DATA)
    mytoken = getToken()
    myresults = getModelResults(mytoken, input_header, input_data)
 
    print(myresults.json())


    print('the end')