import pymongo
import pandas as pd

mongo_client = pymongo.MongoClient("mongodb://mongodb1:27017/")

db = mongo_client["sensor_data_db"]
collection = db["sensors"]

df = pd.read_csv('/app/sensor_data.csv')

data_dict = df.to_dict("records")
collection.insert_many(data_dict)

print("Data loaded successfully into MongoDB!")
