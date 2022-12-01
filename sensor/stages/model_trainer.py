
"""
from sensor.utils.main_utils import load_numpy_array,load_object,save_object
from sensor.exception import CustomException

from sensor.logger import logging
from sensor.entity.artifacts import DataTransformationArtifacts,ModelTrainerArtifacts
from sensor.entity.config import ModelTrainerConfig
from xgboost import XGBClassifier
import os,sys
from sensor.MachineLearning.Metrics.classification_metric import get_classification_score
from sensor.MachineLearning.model.estimator import SensorModel
class ModelTraining:
    def __init__(self,model_trainer_config=ModelTrainerConfig,data_transformation_artifacts=DataTransformationArtifacts):

        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts
            
        except Exception as e:
            raise CustomException(e,sys)
    
    def perform_tuning(self):
        pass
        
    def train_model(self,X_train,y_train):
        try:
            clf = XGBClassifier()
            clf.fit(X_train,y_train)
            return clf
        except Exception as e:
            raise CustomException(e,sys)
    
        
        
    def  start_model_training(self)-> ModelTrainerArtifacts:
        try:
            test_file_path= self.data_transformation_artifacts.transformed_test_file_path
            train_file_path = self.data_transformation_artifacts.transformed_training_file_path

            #loading train and test file
            train_array = load_numpy_array(train_file_path)
            test_array = load_numpy_array(test_file_path)
            

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )


            model = self.train_model(X_train,y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_score = get_classification_score(y_true=y_train,y_pred=y_train_pred)

            if train_score.f1_score <= self.model_trainer_config.model_accuracy:
                raise Exception("Trained model is not efficient to provide expected results")


            test_score =  get_classification_score(y_true=y_test,y_pred=y_test_pred)

            # Now, check for the overfitting and underfitting

            diff =  abs(train_score.f1_score - test_score.f1_score)

            threshold = 0.05

            if diff > threshold:
                raise Exception("Model is not good. need more tuning")
            
            preprocessor = load_object(file_path=self.data_transformation_artifacts.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained__model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            sensor_model = SensorModel(preprocessor=preprocessor,model=model)

            save_object(self.model_trainer_config.trained__model_file_path,obj=sensor_model)

            ## Model Trainer artifacts

            modeltrainerartifacts =  ModelTrainerArtifacts(trained__model_file_path=self.model_trainer_config.trained__model_file_path,train_metric_artifacts=train_score,test_metric_artifacts=test_score)
            logging.info(f"Model Trainer Artifcats stored at {modeltrainerartifacts} ")
            return modeltrainerartifacts

            



        except Exception as e:
            raise CustomException(e,sys)
            
            
            """



from sensor.utils.main_utils import load_numpy_array
from sensor.exception import CustomException
from sensor.logger import logging
from sensor.entity.artifacts import DataTransformationArtifacts,ModelTrainerArtifacts
from sensor.entity.config import ModelTrainerConfig
import os,sys
from xgboost import XGBClassifier
from sensor.MachineLearning.Metrics.classification_metric import get_classification_score
from sensor.MachineLearning.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object

class ModelTrainer:

    def __init__(self,model_trainer_config:ModelTrainerConfig,
        data_transformation_artifact:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def perform_hyper_paramter_tunig(self):...
    

    def train_model(self,x_train,y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
        except Exception as e:
            raise e
    
    def initiate_model_trainer(self)->ModelTrainerArtifacts:
        try:
            train_file_path = self.data_transformation_artifact.transformed_training_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            print(train_file_path)
            #loading training array and testing array
            train_arr = load_numpy_array(file_path = train_file_path)
            test_arr = load_numpy_array(file_path = test_file_path)
            print(train_arr)
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)
            classification_train_metric =  get_classification_score(y_true=y_train, y_pred=y_train_pred)
            
            if classification_train_metric.f1_score<=self.model_trainer_config.model_accuracy:
                raise Exception("Trained model is not good to provide expected accuracy")
            
            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)


            #Overfitting and Underfitting
            diff = abs(classification_train_metric.f1_score-classification_test_metric.f1_score)
            
            if diff>self.model_trainer_config.model_accuracy:
                raise Exception("Model is not good try to do more experimentation.")

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained__model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            sensor_model = SensorModel(preprocessor=preprocessor,model=model)
            save_object(self.model_trainer_config.trained__model_file_path, obj=sensor_model)

            #model trainer artifact

            model_trainer_artifact = ModelTrainerArtifacts(trained__model_file_path=self.model_trainer_config.trained__model_file_path, 
            train_metric_artifacts=classification_train_metric,
            test_metric_artifacts=classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
