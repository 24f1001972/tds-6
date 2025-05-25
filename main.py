from fastapi import FastAPI, Query
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

#Enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the path to the JSON file
current_directory = os.path.dirname(__file__)  # Directory of main.py
json_file_path = os.path.join(current_directory, 'data/q-vercel-python.json')

# Load the JSON file
try:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = []  # Provide a fallback in case the file is missing
except json.JSONDecodeError:
    data = []  # Handle invalid JSON format

@app.get("/")
def read_home():
    return {"message": "Homepage"}

@app.get("/api")
def read_csv(name: List[str] = Query(None)):
    if not name:
        return {"error": "No names provided!"}
    
    marks_list = []
    for query_name in name:
        found_user = next((user for user in data if user.get("name") == query_name), None)
        if found_user:
            marks_list.append(found_user.get("marks", None))
        else:
            marks_list.append(None)  # or 0 or -1 or any placeholder
    
    return {"marks": marks_list}
    