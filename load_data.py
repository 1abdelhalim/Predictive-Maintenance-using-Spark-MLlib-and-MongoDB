import pymongo
import pandas as pd

# MongoDB connection string
mongo_client = pymongo.MongoClient("mongodb://mongodb1:27017/")

# Access the database and collection
db = mongo_client["sensor_data_db"]
collection = db["sensors"]

# Load your sensor data CSV
df = pd.read_csv('/app/sensor_data.csv')

# Convert the dataframe to a dictionary and insert it into MongoDB
data_dict = df.to_dict("records")
collection.insert_many(data_dict)

print("Data loaded successfully into MongoDB!")
