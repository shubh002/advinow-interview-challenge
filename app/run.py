import uvicorn
from fastapi import FastAPI # need python-multipart
from views import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AdviNow Interview Challenge", version="1.6")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8013)
