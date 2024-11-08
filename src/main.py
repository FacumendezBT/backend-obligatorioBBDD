from fastapi import FastAPI
from controllers.instructores import router as instructores_router

app = FastAPI()

app.include_router(instructores_router, prefix="/instructores", tags=["Instructores"])

