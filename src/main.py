from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.instructores import router as instructores_router
from controllers.alumnos import router as alumnos_router
from controllers.clases import router as clases_router
from controllers.users import router as users_router
from middlewares.auth import AuthMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

app.include_router(
    instructores_router, prefix="/api/instructores", tags=["Instructores"]
)
app.include_router(alumnos_router, prefix="/api/alumnos", tags=["Alumnos"])
app.include_router(clases_router, prefix="/api/clases", tags=["Clases"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
