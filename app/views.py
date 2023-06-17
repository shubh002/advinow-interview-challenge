from fastapi import APIRouter,UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import os
import csv
from models import BusinessDataLoader
from models import Business, Symptom, SessionLocal

business_data_loader = BusinessDataLoader()
router = APIRouter()

@router.get('/')
async def get_index():
    return FileResponse("views/index.html")


@router.post("/upload")
async def upload_file(file: UploadFile = UploadFile(...)):
    try:
        contents = await file.read()  # Read the contents of the uploaded file
        decoded_contents = contents.decode("utf-8")  # Decode the contents assuming UTF-8 encoding
        
        csv_data = []
        reader = csv.reader(decoded_contents.splitlines(), delimiter=',')
        for row in reader:
            csv_data.append(row)
        if len(csv_data) > 0:
            business_data_loader.update(csv_data)
            return JSONResponse(content={"message": "DB sucessfully updated"}, status_code=200, media_type="application/json")
        else:
            return JSONResponse(content={"message": "looks like the file is empty or corrupt"}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/data")
async def get_data(business_id: int = None, diagnostic: bool = None):
    results = {}
    session = SessionLocal()
    # Check if business_id is provided
    
    print(business_id)

    if business_id is not None:
        temp = session.query(Business, Symptom). \
                filter(Business.business_id == business_id). \
                filter(Business.symptom_code == Symptom.symptom_code).all()
        for t in temp:
            print(dir(t))

    
        
    # Return the results
    # return results

@router.get('/status')
async def get_status():
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}
