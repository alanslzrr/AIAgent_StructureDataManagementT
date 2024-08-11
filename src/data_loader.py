import pymongo
import streamlit as st

@st.cache_resource
def setup_mongodb():
    uri = "mongodb+srv://alanslzr:alanslzr@clusterphoenix.ffv0t.mongodb.net/?retryWrites=true&w=majority&appName=ClusterPhoenix"
    client = pymongo.MongoClient(uri)
    db = client["calibration_database"]
    collection = db["calibration_data"]
    return collection