import uvicorn
from fastapi import FastAPI

import models
from database import engine
from Routers import Users

models.Base.metadata.create_all(bind=engine)

app =FastAPI(title="mYaPP", description="mYaPP",
             verion="1.0.0")

app.include_router(Users.router)

@app.get("/")
def root():
    return {"massage": "eier"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)