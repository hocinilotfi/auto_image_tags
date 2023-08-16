from fastapi import FastAPI,UploadFile, File
import numpy as np
import cv2
from PIL import Image

from app.ml_model import yolo3

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello from Lotfi App!"}


#to run the app: >   uvicorn app.main:app --reloadfrom

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    # Read the uploaded image
    image = await file.read()
   
    respons = yolo3.process_image(image)
    print(respons)
    # Prepare JSON response
    response_data = {
       'data' : respons
    }
    
    return response_data
