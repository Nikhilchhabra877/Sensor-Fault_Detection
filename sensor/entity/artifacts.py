from dataclasses import dataclass

@dataclass
class DataIngestingArtifacts:
    training_file_path: str
    testing_file_path: str

@dataclass

class DataValidationArtifacts:
    validation_status : bool
    valid_training_file_path : str
    valid_testing_file_path : str
    invalid_training_file_path : str
    invalid_testing_file_path : str
    drift_report_file_path : str

@dataclass

class DataTransformationArtifacts:

    transformed_object_file_path : str
    transformed_training_file_path : str
    transformed_test_file_path : str

@dataclass

class ClassificationMetricArtifacts:
    f1_score : float
    precision_score : float
    recall_score : float

@dataclass
class ModelTrainerArtifacts:
    trained__model_file_path : str
    train_metric_artifacts : ClassificationMetricArtifacts
    test_metric_artifacts : ClassificationMetricArtifacts

@dataclass
class ModelEvaluationArtifacts:
    is_model_accepted :bool 
    improved_accuracy : float
    best_model_path : str
    trained_model_path : str
    trained_model_metric_artifacts : ClassificationMetricArtifacts
    best_model_metric_artifacts : ClassificationMetricArtifacts


@dataclass
class ModelPusherArtifact:
    saved_model_path:str
    model_file_path:str