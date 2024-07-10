import os
import sys
from src.footballproject.logger import logging
from src.footballproject.exception import CustomException
from src.footballproject.components.data_ingestion import DataIngestion
from src.footballproject.components.data_transformation import DataTransformation
from src.footballproject.components.model_trainer import ModelTrainer
import pandas as pd
import uvicorn
from fastapi import FastAPI
import pickle
from FootballFeature import FootballFeature



app = FastAPI()
with open("artifact/preprocessor.pkl", "rb") as preprocessor_in:
    preprocessor = pickle.load(preprocessor_in)

with open("artifact/model.pkl", "rb") as model_in:
    classifier = pickle.load(model_in)


@app.get('/')
def index():
    return {'message': 'Welcome!'}


@app.post('/predict')
def predict_result(data:FootballFeature):
    data = data.dict()
    
    data_f = {
    'Home_Fatigue': data['Home_Fatigue'],
    'Away_Fatigue': data['Away_Fatigue'],
    'Temp': data['Temp'],
    'Humidity': data['Humidity'],
    'Wind': data['Wind'],
    'Referee_Bias': data['Referee_Bias'],    
    'xG_Home': data['xG_Home'],
    'xG_Away': data['xG_Away'],
    'xGA_Home': data['xGA_Home'],
    'xGA_Away': data['xGA_Away'],

    }

    data_f = pd.DataFrame([data_f])

    data_f['xG_Diff'] = data_f['xG_Home'] - data_f['xG_Away']
    data_f['xGA_Diff'] = data_f['xGA_Home'] - data_f['xGA_Away']

    data_f['xGA_Ratio_Home'] = data_f['xGA_Home'] / (data_f['xG_Home'] + 0.1)
    data_f['xGA_Ratio_Away'] = data_f['xGA_Away'] / (data_f['xG_Away'] + 0.1)



    data_features = preprocessor.transform(data_f)  
    prediction = classifier.predict(data_features)[0]
    return {
        'prediction': prediction
    }


# if __name__ == "__main__":
#     uvicorn.run(app)




    