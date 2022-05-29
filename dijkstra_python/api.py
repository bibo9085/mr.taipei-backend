import flask
from flask import jsonify, request, make_response
# from flask_cors import CORS
import numpy as np
import pandas as pd
import cv2
x = float('inf')
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = True
def getSpotPosition(stationName):
    spotPosition = pd.read_csv("stationSpotPosition/spotPosition_"+ stationName +".csv", encoding="Big5")
    spotFull_list = []
    spotPosition_list = []
    nrows = spotPosition.shape[0]
    for i in range(nrows):
        ser = spotPosition.loc[i, :]
        row_dict = []
        for idx, val in zip(ser.index[1:3], ser.values[1:3]):
            if type(val) is str:
                row_dict.append(val)
            elif type(val) is np.int64:
                row_dict.append(int(val))
            elif type(val) is np.float64:
                row_dict.append(float(val))
        spotPosition_list.append(row_dict)
        row_dict2 = {}
        for idx, val in zip(ser.index[:3], ser.values[:3]):
            if type(val) is str:
                row_dict2[idx] = val
            elif type(val) is np.int64:
                row_dict2[idx] = int(val)
            elif type(val) is np.float64:
                row_dict2[idx] = float(val)
        spotFull_list.append(row_dict2)
        # print(spotFull_list)
    spotBranch_list = []
    for i in range(nrows):
        ser = spotPosition.loc[i]
        row_dict = []
        # count = 0
        for idx, val in zip(ser.index[3:], ser.values[3:]):
            # count += 1
            if val == 'x':
                row_dict.append(float('inf'))
            else :
                row_dict.append(int(val))
        spotBranch_list.append(row_dict)
        # print(spotBranch_list)
    return spotPosition_list, spotFull_list, spotBranch_list

app.run

