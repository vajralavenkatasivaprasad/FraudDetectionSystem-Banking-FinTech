from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType
import joblib
import pandas as pd
model = joblib.load("../ml/fraud_model.pkl")
spark = SparkSession.builder.appName("FraudDetection").getOrCreate()
# Add schema and streaming logic here
