from fastapi import FastAPI
from controllers.instructores import router as instructores_router
from controllers.alumnos import router as alumnos_router
from controllers.clases import router as clases_router
from controllers.users import router as users_router

app = FastAPI()

app.include_router(instructores_router, prefix="/instructores", tags=["Instructores"])
app.include_router(alumnos_router, prefix="/alumnos", tags=["Alumnos"])
app.include_router(clases_router, prefix="/clases", tags=["Clases"])
app.include_router(users_router, prefix="/users", tags=["Users"])

