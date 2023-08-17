from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware 
import numpy as np
import cv2
from PIL import Image

from app.ml_model import yolo3

app = FastAPI()
# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",  # Add the URL of your React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello from Lotfi App!"}


# to run the app: >   uvicorn app.main:app --reload


@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    # Read the uploaded image
    image = await file.read()

    respons = yolo3.process_image(image)
    print(respons)
    # Prepare JSON response
    response_data = {"data": respons}

    return response_data
