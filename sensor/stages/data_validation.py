from sensor.constants.training_pipeline import SCHEMA
from sensor.entity.artifacts import DataIngestingArtifacts,DataValidationArtifacts
from sensor.entity.config import DataValidationConfig
from sensor.exception import CustomException
from sensor.logger import logging
import pandas as pd
import os,sys
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from scipy import stats

class DataValidation:

    def __init__(self,data_ingestion_artifacts : DataIngestingArtifacts,data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA)
        except Exception as e:
            raise CustomException(e,sys)
    

    

    def check_no_of_columns(self,dataframe:pd.DataFrame)->bool:
        
        
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])

            #print(len(dataframe.columns))
            #print(len(self._schema_config["columns"]))

            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise CustomException(e,sys)



    def check_numerical_column(self,dataframe:pd.DataFrame)->bool:
        try:
          #num_columns = len(self._schema_config["columns"])
          df_col = dataframe.columns

          flag = True
          missing_num_cols = []
          for column in self._schema_config["numerical_columns"]:
              if column not in df_col:
                  flag = False
                  missing_num_cols.append(column)

          logging.info(f"Missing numerical columns :[{flag}]")      
          return flag
        except Exception as e:
            raise CustomException(e,sys)


    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

        
    def capture_data_drift(self,base_df,target_df,threshold = 0.5)-> bool:

        try:

            status = True
            report = {}

            for col in base_df.columns:
                d1 = base_df[col]
                d2 = target_df[col]
                check_dist = stats.ks_2samp(d1,d2)

                if threshold <= check_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False

                report.update({col: {"P-value":float(check_dist.pvalue),"Drift_Status" :is_found }}) 

            drift_report_File_Path = self.data_validation_config.drift_report_file_path
            create_dir =  os.path.dirname(drift_report_File_Path)
            os.makedirs(create_dir,exist_ok=True)
            write_yaml_file(file_path=drift_report_File_Path,content=report)
        
            return status
        except Exception as e:
            raise CustomException(e,sys)       

    def start_data_validation(self)->DataIngestingArtifacts:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifacts.training_file_path
            test_file_path = self.data_ingestion_artifacts.testing_file_path

            "Reading data from train and test file location"
            train_data = DataValidation.read_data(train_file_path)
            test_data =  DataValidation.read_data(test_file_path)

            "validate number of columns"
            status = self.check_no_of_columns(dataframe=train_data)
            #print(status)
            if not status:
                error_message = f"{error_message} No. of columns are not matching"
            self.check_no_of_columns(dataframe=test_data)

            status = self.check_no_of_columns(dataframe=test_data)
            #print(status)
            if not status:
                error_message = f"{error_message} No. of columns are not matching"

            "check and validate numerical columns"

            status = self.check_numerical_column(dataframe=train_data)
            if not status:
                error_message = f"{error_message} train data does not contain all numerical columns"


            status = self.check_numerical_column(dataframe=test_data)
            if not status:
                error_message = f"{error_message} test data does not contain all numerical columns"

            if len(error_message) > 0:
                raise Exception(error_message)
            
            "Check Data Drift"

            status =  self.capture_data_drift(base_df = train_data,target_df=test_data)

            data_validation_artifacts = DataValidationArtifacts(
                
                validation_status  = status,
                valid_training_file_path = self.data_ingestion_artifacts.training_file_path,
                valid_testing_file_path = self.data_ingestion_artifacts.testing_file_path,
                #invalid_training_file_path =  self.data_validation_config.invalid_train_file_path,
                #invalid_testing_file_path = self.data_validation_config.invalid_test_file_path,
                invalid_training_file_path = None,
                invalid_testing_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path

            
            )
            logging.info(f"Data validation Artifacts: {data_validation_artifacts}")
        except Exception as e:
            raise CustomException(e,sys)