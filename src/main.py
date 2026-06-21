import uvicorn
from fastapi import FastAPI

from src.routers import users, swipes
from src.database import engine
from src.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Finnldy API",
    description="REST-API für die Gruppen-Filmempfehlungs-App Finnldy",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(swipes.router)


@app.get("/")
def root():
    return {
        "message": "Passt"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)