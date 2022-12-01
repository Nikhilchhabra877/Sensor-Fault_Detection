from sensor.entity.artifacts import ClassificationMetricArtifacts
from sensor.exception import CustomException
from sensor.logger import logging
import os,sys
from sklearn.metrics import f1_score,precision_score,recall_score

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifacts:

    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classsification_metric =  ClassificationMetricArtifacts(f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        return classsification_metric
    except Exception as e:
        raise CustomException(e,sys)