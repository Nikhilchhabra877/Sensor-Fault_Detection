import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sensor.constants.training_pipeline import TARGET_NAME
from sensor.entity.artifacts import(DataTransformationArtifacts,DataValidationArtifacts,DataIngestingArtifacts)

from sensor.entity.config import DataTransformationConfig
from sensor.exception import CustomException
from sensor.logger import logging

from sensor.MachineLearning.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array,save_object


class DataTransformation:
    def __init__(self,data_validation_artifacts :DataValidationArtifacts, data_transformation_config:DataTransformationConfig):
    
        try:

            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config 
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:

        try:

            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    @classmethod
    def get_data_transformer_object(cls)-> Pipeline:

        try:

            rb_scaler = RobustScaler() ## it is used to keep every feature in same range and handle outliers
            simple_impute = SimpleImputer(strategy="constant",fill_value=0) # replace missing values with zero
            preprocessor = Pipeline(steps=[("Simple_Imputer",simple_impute),("Robust_scaler",rb_scaler)])
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        


    def start_data_transformation(self)->DataTransformationArtifacts:
        try:

           # print(self.data_validation_artifacts.valid_training_file_path)

            training_data = DataTransformation.read_data(file_path = self.data_validation_artifacts.valid_training_file_path)
            testing_data = DataTransformation.read_data(file_path = self.data_validation_artifacts.valid_training_file_path)
            preprocessor = self.get_data_transformer_object()


            ## Transformation of training data_frame
            input_train_dataframe = training_data.drop(columns=[TARGET_NAME],axis=1)
            target_input_train = training_data[TARGET_NAME]
            target_input_train =  target_input_train.replace(TargetValueMapping().to_dict())

            ## Transformation of testing data_frame

            input_test_dataframe = testing_data.drop(columns=[TARGET_NAME],axis=1)
            target_input_test = testing_data[TARGET_NAME]
            target_input_test =  target_input_test.replace(TargetValueMapping().to_dict())

            ## call fit method

            ## training
            preprocessor_obj = preprocessor.fit(input_train_dataframe)
            transformed_input_data_training = preprocessor_obj.transform(input_train_dataframe)
            ## testing 
            transformed_input_data_testing = preprocessor_obj.transform(input_test_dataframe)

            smote = SMOTETomek(sampling_strategy="minority")

            final_training_input_data,target_final_training_input_data = smote.fit_resample(transformed_input_data_training,target_input_train)
            final_testing_input_data,target_final_testing_input_data = smote.fit_resample(transformed_input_data_testing,target_input_test)

            ## Now combine training and testing df with target

            train_data = np.c_[final_training_input_data,np.array(target_final_training_input_data)]
            test_data = np.c_[final_testing_input_data,np.array(target_final_testing_input_data)]

            ## Now, save numpy data

            save_numpy_array(self.data_transformation_config.transformed_training_file_path,array=train_data)

            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array=test_data)

            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)

            data_transformation_artifacts =  DataTransformationArtifacts(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_training_file_path = self.data_transformation_config.transformed_training_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path)

            logging.info(f"Data transformation completed successfully at {data_transformation_artifacts} ")
            return data_transformation_artifacts
        except Exception as e:
            raise CustomException(e,sys)

    

  