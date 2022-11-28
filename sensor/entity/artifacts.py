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

class DataTransformationArtifacts:

    transformed_object_file_path : str
    transformed_training_file_path : str
    transformed_test_file_path : str