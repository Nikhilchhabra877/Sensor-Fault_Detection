from sensor.exception import CustomException
from sensor.logger import logging
from sensor.entity.artifacts import DataValidationArtifacts,ModelTrainerArtifacts,ModelEvaluationArtifacts
from sensor.entity.config import ModelEvaluationConfig
import os,sys
from sensor.MachineLearning.Metrics.classification_metric import get_classification_score
from sensor.MachineLearning.model.estimator import SensorModel
from sensor.utils.main_utils import load_object,write_yaml_file,save_object
from sensor.MachineLearning.model.estimator import ModelReolver
from sensor.constants.training_pipeline import TARGET_NAME
from sensor.MachineLearning.model.estimator import TargetValueMapping
import pandas  as  pd

class ModelEvaluation:


    def __init__(self,model_eval_config:ModelEvaluationConfig,
                    data_validation_artifact:DataValidationArtifacts,
                    model_trainer_artifact:ModelTrainerArtifacts):
        
        try:
            self.model_eval_config=model_eval_config
            self.data_validation_artifact=data_validation_artifact
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
    


    def initiate_model_evaluation(self)->ModelEvaluationArtifacts:
        try:
            valid_train_file_path = self.data_validation_artifact.valid_training_file_path
            valid_test_file_path = self.data_validation_artifact.valid_testing_file_path

            #valid train and test file dataframe
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df,test_df])
            y_true = df[TARGET_NAME]
            y_true.replace(TargetValueMapping().to_dict(),inplace=True)
            df.drop(TARGET_NAME,axis=1,inplace=True)

            train_model_file_path = self.model_trainer_artifact.trained__model_file_path
            model_resolver = ModelReolver()
            is_model_accepted=True


            if not model_resolver.is_model_exists():
                model_evaluation_artifacts = ModelEvaluationArtifacts(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=None, 
                    best_model_path=None, 
                    trained_model_path=train_model_file_path, 
                    trained_model_metric_artifacts=self.model_trainer_artifact.test_metric_artifacts, 
                    best_model_metric_artifacts=None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifacts}")
                return model_evaluation_artifacts

            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=train_model_file_path)
            
            y_trained_pred = train_model.predict(df)
            y_latest_pred  = latest_model.predict(df)

            trained_metric = get_classification_score(y_true, y_trained_pred)
            latest_metric = get_classification_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.f1_score-latest_metric.f1_score
            if self.model_eval_config.change_threshold < improved_accuracy:
                #0.02 < 0.03
                is_model_accepted=True
            else:
                is_model_accepted=False

            
            model_evaluation_artifact = ModelEvaluationArtifacts(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=improved_accuracy, 
                    best_model_path=latest_model_path, 
                    trained_model_path=train_model_file_path, 
                    trained_model_metric_artifacts=trained_metric, 
                    best_model_metric_artifacts=latest_metric)

            model_eval_report = model_evaluation_artifact.__dict__

            #save the report
            write_yaml_file(self.model_eval_config.report_file_path, model_eval_report)
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise CustomException(e,sys)