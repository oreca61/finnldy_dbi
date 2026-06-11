import uvicorn
from fastapi import FastAPI

import models
from database import engine
from Routers import users

models.Base.metadata.create_all(bind=engine)

app =FastAPI(title="mYaPP", description="mYaPP",
             version="1.0.0")

app.include_router(users.router)

@app.get("/")
def root():
    return {"massage": "Mero hat kleine Eier"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)