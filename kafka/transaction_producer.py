from kafka import KafkaProducer
import json
import pandas as pd
import time
df = pd.read_csv("../data/creditcard.csv").head(100)
for _, row in df.iterrows():
     transaction = row.to_dict()
     producer.send('transactions', transaction)
     print(f"Sent transaction {transaction['Time']}")
     time.sleep(1)
