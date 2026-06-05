# import os
# import sys
# import json
# import pandas as pd
# import certifi
# import numpy as np
# import pymongo
# from networksecurity.exceptions.exception import NetworkSecurityException
# from networksecurity import logger


# from dotenv import load_dotenv
# load_dotenv(override=True)

# MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

# certifi.where()

# class NetworkDataExtract():
#     def __init__(self):
#         try:
#             pass
#         except Exception as e:
#             raise  NetworkSecurityException(e,sys)
    
#     def csv_to_json_convertor(self,file_path):
#         try:    
#             data = pd.read_csv(file_path)
#             data.reset_index(drop=True, inplace=True)
#             records = list(json.loads(data.T.to_json()).values())
#             return records
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def insert_data_mongodb(self,records,database,collection):
#         try:
#             self.database = database
#             self.collection = collection
#             self.records = records

#             self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
#             self.database = self.mongo_client[self.database]

#             self.collection = self.database[self.collection]
#             self.collection.insert_many(self.records)

#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
# if __name__ == '__main__':
#     FILE_PATH = "/Network_Data/Phishing_Legitimate_full.csv"
#     database = "Rajaee"
#     collection = "NetworkData"
#     networkObj = NetworkDataExtract()
#     records = networkObj.csv_to_json_convertor(file_path=FILE_PATH)
#     no_of_records = networkObj.insert_data_mongodb(records,database,collection)
#     print(no_of_records)
        
import os
import sys
import pandas as pd
import sqlite3

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity import logger


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def read_csv(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_sqlite(self, dataframe, database, table):
        try:
            conn = sqlite3.connect(database)

            dataframe.to_sql(
                name=table,
                con=conn,
                if_exists="replace",
                index=False
            )

            conn.commit()
            conn.close()

            return len(dataframe)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == '__main__':

    FILE_PATH = "Network_Data/Phishing_Legitimate_full.csv"
    DATABASE = "networksecurity.db"
    TABLE = "NetworkData"

    networkObj = NetworkDataExtract()

    df = networkObj.read_csv(FILE_PATH)

    no_of_records = networkObj.insert_data_sqlite(
        dataframe=df,
        database=DATABASE,
        table=TABLE
    )

    print(f"{no_of_records} records inserted into SQLite database.")
