import os
import sys
from src.footballproject.exception import CustomException
from src.footballproject.logger import logging
import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X,y,models):
    try:
        report = {}

        for i in range(len(list(models))):
            
            model = list(models.values())[i]
            
            kf = KFold(n_splits=5, shuffle=True, random_state=42)
            scores = []
            
            for train_indices, test_indices in kf.split(X,y):
                X_train, y_train = X[train_indices], y[train_indices]
                X_test, y_test = X[test_indices], y[test_indices]
                
                # Training the model on the training data
                model.fit(X_train, y_train)
                
                # Making predictions on the test data
                y_pred = model.predict(X_test)
                
                # Calculating the accuracy score for this fold
                fold_score = accuracy_score(y_test, y_pred)
                
                # Appending the fold score to the list of scores
                scores.append(fold_score)

                mean_score = np.mean(scores)

            report[list(models.keys())[i]] = mean_score
        
        return report

    except Exception as e:
        raise CustomException(e, sys)
