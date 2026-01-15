import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routes import health, auth

load_dotenv()

app = FastAPI()

app.include_router(
    health.router,
    prefix="/health"
)

app.include_router(
    auth.router,
    tags=["Authentication"],
    prefix="/auth"
)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
