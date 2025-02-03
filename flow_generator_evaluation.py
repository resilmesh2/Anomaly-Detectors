import pandas as pd
from kafka import KafkaProducer
import json
import time
from preprocessor import label_encode
import logging

logger = logging.getLogger('a')

# Load the dataset
df = pd.read_csv("testing_df.csv")

df_sampled = df.drop(columns=["Label"])

# Convert object columns to categorical
object_columns = df_sampled.select_dtypes(include='object').columns
df_sampled[object_columns] = df_sampled[object_columns].astype('category')

# Apply label encoding
df_sampled, encoder = label_encode(df_sampled, logger)

print(df_sampled)
# Convert the DataFrame to JSON lines with required format
df_jsons_list = df_sampled.apply(lambda row: json.dumps({"features": row.tolist()}), axis=1).tolist()

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['155.54.205.196:9092'],
)

# Send the data to the Kafka topic
count = 0
for item in df_jsons_list:
    count += 1
    print(count)
    producer.send("flows-info", value=item.encode('utf-8'))
producer.flush()

print("Data has been sent to Kafka topic successfully.")
