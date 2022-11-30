from sensor.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_NAME
import os,sys
class TargetValueMapping:
    def __init__(self):
        self.neg :int = 0
        self.pos :int = 1

    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        map_reponse =  self.to_dict()
        return dict(zip(map_reponse.values(),map_reponse.keys()))



## check the model accuracy

class SensorModel:

    def __init__(self,preprocessor,model):
        self.preprocessor = preprocessor
        self.model = model
    
    def predict(self,x):

        try:

            X_transform = self.preprocessor.transform(x)
            
            y_pred =self.model.predict(X_transform)

            return y_pred
        except Exception as e:

            raise e


class ModelReolver:
    def __init__(self,model_dir=SAVED_MODEL_DIR):
        
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise e
        
    def get_best_model_path(self):

        try:
            timestamp = list(map(int,os.listdir(self.model_dir)))
            lastest_timestamp = max(timestamp)

            lastest_model_path = os.path.join(self.model_dir,f"{lastest_timestamp}",MODEL_NAME)
            return lastest_model_path

        except Exception as e:
            raise e
        
    
    def is_model_exists(self):

        try:

            if not os.path.exists(self.model_dir):
                return False
            timestamp = os.listdir(self.model_dir)
            if len(timestamp) == 0:
                return False
            
            latest_model_path = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False
            return True
        except Exception as e:
            raise e
        
    