from fastapi import FastAPI
from routes.instructores import router as instructores_router

app = FastAPI()

app.include_router(instructores_router)
