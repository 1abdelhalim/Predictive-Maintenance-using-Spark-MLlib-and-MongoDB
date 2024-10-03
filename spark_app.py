from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

#  Spark session
spark = SparkSession.builder \
    .appName("PredictiveMaintenance") \
    .config("spark.mongodb.input.uri", "mongodb://mongodb1:27017/sensor_data") \
    .config("spark.mongodb.output.uri", "mongodb://mongodb1:27017/sensor_data") \
    .getOrCreate()

# Load data from MongoDB
df = spark.read.format("mongo").load()

assembler = VectorAssembler(inputCols=[
    "Air temperature", "Process temperature", "Rotational speed",
    "Torque", "Tool wear"
], outputCol="features")

data = assembler.transform(df)

train, test = data.randomSplit([0.8, 0.2])

rf = RandomForestClassifier(labelCol="Machine failure", featuresCol="features", numTrees=10)
model = rf.fit(train)

predictions = model.transform(test)

evaluator = MulticlassClassificationEvaluator(labelCol="Machine failure", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

print(f"Test Accuracy: {accuracy}")

# Stop Spark session
spark.stop()
