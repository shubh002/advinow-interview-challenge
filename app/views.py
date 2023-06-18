from fastapi import APIRouter,UploadFile, Query
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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
async def get_data(business_id: int = Query(None, description='Business ID'),
             diagnostic: str = Query(None, description='Diagnostic')):

    session = SessionLocal()
    
    # business_id = request.args.get('business_id')
    # diagnostic = request.args.get('symptom_diagnostic')

    query = session.query(Business.business_id, Business.business_name, Business.symptom_code,
                             Symptom.symptom_name, Symptom.symptom_diagnostic)

    # Check if business_id is provided
    if business_id:
        query = query.filter(Business.business_id == business_id)

    # Check if symptom diagnostic is provided
    if diagnostic:
        query = query.filter(Symptom.symptom_diagnostic == diagnostic)
    
    query = query.join(Symptom, Business.symptom_code == Symptom.symptom_code)

    result = query.all()

    data = []
    for row in result:
        business_id, business_name, symptom_code, symptom_name, symptom_diagnostic = row
        data.append({
            'business_id': business_id,
            'business_name': business_name,
            'symptom_code': symptom_code,
            'symptom_name': symptom_name,
            'symptom_diagnostic': symptom_diagnostic
        })

    return jsonable_encoder(data)


@router.get('/status')
async def get_status():
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}
