from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from routes import router

load_dotenv()

username = quote_plus(os.getenv('MONGODB_USERNAME'))
password = quote_plus(os.getenv('MONGODB_PASSWORD'))

app = FastAPI()

app.include_router(router, prefix="/api", tags=["api"])

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(f"mongodb+srv://{username}:{password}@ppds.kg0g4.mongodb.net/?retryWrites=true&w=majority&appName=PPDS")
    app.database = app.mongodb_client["PPDS"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()