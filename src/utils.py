import numpy as np
import pandas as pd
import dill
import os
import sys
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, X_test, y_train, y_test, models, param):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]
            grid = GridSearchCV(model, para, cv=3)
            grid.fit(X_train, y_train)
            model.set_params(**grid.best_params_)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            model_score = r2_score(y_test, y_pred)
            report[list(models.keys())[i]] = model_score
        return report
    except Exception as e:
        raise CustomException(e, sys)