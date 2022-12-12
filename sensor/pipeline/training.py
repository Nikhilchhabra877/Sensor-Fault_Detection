from sensor.entity.config import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelPusherConfig,ModelEvaluationConfig
from sensor.exception import CustomException
import os,sys
from sensor.logger import logging
from sensor.entity.artifacts import DataIngestingArtifacts,DataValidationArtifacts,DataTransformationArtifacts,ModelTrainerArtifacts,ModelEvaluationArtifacts
from sensor.stages.data_ingestion import DataIngestion
from sensor.stages.data_validation import DataValidation
from sensor.stages.data_transformation import DataTransformation

from sensor.stages.model_trainer import ModelTrainer
from sensor.stages.model_evaluation import ModelEvaluation
from sensor.stages.model_pusher import ModelPusher
from sensor.storage_s3.s3_sync import S3Sync

from sensor.constants.S3_bucket import TRAINING_BUCKET,PREDICTION_BUCKET
from sensor.constants.training_pipeline import SAVED_MODEL_DIR
class TrainingPipeLine:
    is_pipeline_running = False
    def __init__(self):

        

        training_pipeline =  TrainingPipelineConfig()
        self.data_ingestion = DataIngestionConfig(train_pipeline_config=training_pipeline)
        self.training_pipeline = training_pipeline
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline)
        self.s3_sync = S3Sync()


    def Data_Ingestion(self)->DataIngestingArtifacts:

        try:
            logging.info("staring data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion)
            data_ingestion_artifacts =  data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion completed successfully and artifacts: {data_ingestion_artifacts}")
            return data_ingestion_artifacts
            
        except Exception as e:
            raise CustomException(e,sys)
    """
    def Data_validation(self,data_ingestion_artifacts:DataIngestingArtifacts)-> DataValidationArtifacts:

        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline)
            data_validation = DataValidation(data_ingestion_artifacts=data_ingestion_artifacts,data_validation_config = data_validation_config)
            data_validation_articats = data_validation.start_data_validation()
        except Exception as e:
            raise CustomException(e,sys)
    """

    def Data_Validation(
        self, data_ingestion_artifacts: DataIngestingArtifacts) -> DataValidationArtifacts:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifacts=data_ingestion_artifacts,
                data_validation_config=self.data_validation_config
            )

            data_validation_artifacts = data_validation.start_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e

    def Data_Transformation(self,data_validation_artifacts:DataValidationArtifacts):

        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline)
            data_transformed = DataTransformation(data_validation_artifacts=data_validation_artifacts,data_transformation_config=data_transformation_config)

            data_transformation_artifacts = data_transformed.start_data_transformation()

            return data_transformation_artifacts
        
        except Exception as e:
            raise CustomException(e,sys)

    def Model_trainer(self, data_transformation_artifacts:DataTransformationArtifacts)->ModelTrainerArtifacts:

        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifacts)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except  Exception as e:
            raise  CustomException(e,sys)


    
    def Model_evaluation(self,data_validation_artifacts:DataValidationArtifacts,model_trainer_artifacts:ModelTrainerArtifacts,):

        try:
            model_eval_config = ModelEvaluationConfig(self.training_pipeline)
            model_eval = ModelEvaluation(model_eval_config, data_validation_artifacts, model_trainer_artifacts)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            return model_eval_artifact
        except  Exception as e:
            raise  CustomException(e,sys)

    def Model_Push(self,model_eval_artifacts:ModelEvaluationArtifacts):

        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline)
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifacts)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except  Exception as e:
            raise  CustomException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET}/artifacts/{self.training_pipeline.timestamp}"
            self.s3_sync.sync_dir_to_s3(folder = self.training_pipeline.artifacts_dir,aws_buket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
            
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_dir_to_s3(folder = SAVED_MODEL_DIR,aws_buket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)


    def Run_Pipeline(self):

        try:

            TrainingPipeLine.is_pipeline_running = True
            data_ingestion_artifacts = self.Data_Ingestion()
            data_validation_artifacts = self.Data_Validation(data_ingestion_artifacts=data_ingestion_artifacts)

            data_transformation_artifacts = self.Data_Transformation(data_validation_artifacts=data_validation_artifacts)

            #model_trainer_artifacts = self.Model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            model_trainer_artifacts = self.Model_trainer(data_transformation_artifacts)
            model_eval_artifact = self.Model_evaluation(data_validation_artifacts, model_trainer_artifacts)

            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifacts = self.Model_Push(model_eval_artifact)
            TrainingPipeLine.is_pipeline_running = False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainingPipeLine.is_pipeline_running = False
            raise CustomException(e,sys)



