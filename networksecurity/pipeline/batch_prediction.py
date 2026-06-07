import os
import sys
import pandas as pd
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity import logger
from networksecurity.utils.main_utils import load_object

class PredictPipeline:
    def __init__(self):
        try:
            self.model_path = os.path.join("final_model", "model.pkl")
            self.preprocessor_path = os.path.join("final_model", "preprocessor.pkl")

            logger.info(f"Loading model from {self.model_path}")
            logger.info(f"Loading preprocessor from {self.preprocessor_path}")

            self.model = load_object(self.model_path)
            self.preprocessor = load_object(self.preprocessor_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, features: pd.DataFrame):
        try:
            logger.info("Starting preprocessing for prediction")
            data_scaled = self.preprocessor.transform(features)
            logger.info("Preprocessing completed")

            predictions = self.model.predict(data_scaled)
            logger.info("Prediction completed")

            return predictions

        except Exception as e:
            raise NetworkSecurityException(e, sys)


class CustomData:
    """
    این کلاس ورودی تک نمونه یا چند نمونه را دریافت و به DataFrame تبدیل می‌کند.
    """

    def __init__(self, **kwargs):
        self.data = kwargs

    def get_data_frame(self):
        try:
            df = pd.DataFrame([self.data])
            logger.info("Input data converted to DataFrame")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
