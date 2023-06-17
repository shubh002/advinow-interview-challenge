import uvicorn
from fastapi import FastAPI # need python-multipart
from views import router

app = FastAPI(title="AdviNow Interview Challenge", version="1.6")

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8013)
