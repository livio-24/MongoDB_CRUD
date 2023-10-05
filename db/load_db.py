from pprint import pprint
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017")

db = client["hotels_reviews"]
collection = db["review"]

if collection.count_documents({}) == 0:
    df = pd.read_csv("./data/cleaned_hotels_reviews.csv")
    documents = df.to_dict(orient="records")
    collection.insert_many(documents)

print(f"Number of documents:{collection.count_documents({})}")

cursor = collection.find(limit=5)
for document in cursor:
    pprint(document)
