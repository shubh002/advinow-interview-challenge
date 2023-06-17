from fastapi import APIRouter,UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import os
import csv
from models import Example, SessionLocal

router = APIRouter()

@router.get('/')
async def get_index():
    print("listing dir ; ",os.listdir("./"))
    print(Example)
    db = SessionLocal()
    db_item = Example(business_id = 123, business_name = "asda", symptom_code = "asda", symptom_name = "oeig", symptom_diagnostic =  True)
    db.add(db_item)  # Add the item to the session
    db.commit()  # Commit the changes to the database
    db.refresh(db_item)  # Refresh the item to get the updated values

    return FileResponse("views/index.html")


@router.post("/upload")
async def upload_file(file: UploadFile = UploadFile(...)):
    try:
        contents = await file.read()  # Read the contents of the uploaded file
        decoded_contents = contents.decode("utf-8")  # Decode the contents assuming UTF-8 encoding
        
        # Process the decoded contents
        # Example: Read the CSV data
        csv_data = []
        reader = csv.reader(decoded_contents.splitlines(), delimiter=',')
        for row in reader:
            csv_data.append(row)
        
        # Return a JSON response with the processed data
        print("csv_data : ",csv_data)
        # return JSONResponse(content={"data": csv_data}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get('/status')
async def get_status():
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}
