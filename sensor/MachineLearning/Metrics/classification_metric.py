from sensor.entity.artifacts import ClassificationMetricArtifacts
from sensor.exception import CustomException
from sensor.logger import logging
from sklearn.metrics import f1_score,precision_score,recall_score

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifacts:

    try:
        f1_score = f1_score(y_true,y_pred)
        precision_score = precision_score(y_true,y_pred)
        recall_score = recall_score(y_true,y_pred)

        results = ClassificationMetricArtifacts(f1_score=f1_score,precision_score=precision_score,recall_score=recall_score)

        return results

    except Exception as e:
        raise C