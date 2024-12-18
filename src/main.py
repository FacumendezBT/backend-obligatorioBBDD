from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.instructores import router as instructores_router
from controllers.alumnos import router as alumnos_router
from controllers.clases import router as clases_router
from controllers.users import router as users_router
from controllers.turnos import router as turnos_router
from controllers.equipamiento import router as equipamiento_router
from controllers.actividades import router as actividades_router
from controllers.reportes import router as reportes_router
from middlewares.admin import AdminMiddleware
from middlewares.auth import AuthMiddleware
from contextlib import asynccontextmanager
from db.connection_pool import ConnectionPool


@asynccontextmanager
async def lifespan(app: FastAPI):
    ConnectionPool.init()
    yield
    ConnectionPool.shutdown()


app = FastAPI(lifespan=lifespan)
app.add_middleware(AdminMiddleware)
app.add_middleware(AuthMiddleware)

app.add_middleware(AdminMiddleware)
app.add_middleware(AuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    instructores_router, prefix="/api/instructores", tags=["Instructores"]
)
app.include_router(alumnos_router, prefix="/api/alumnos", tags=["Alumnos"])
app.include_router(clases_router, prefix="/api/clases", tags=["Clases"])
app.include_router(users_router, prefix="/api/usuarios", tags=["Users"])
app.include_router(turnos_router, prefix="/api/turnos", tags=["Turnos"])
app.include_router(equipamiento_router, prefix="/api/equipamiento", tags=["Equipamiento"])
app.include_router(actividades_router, prefix="/api/actividades", tags=["Actividades"])
app.include_router(reportes_router, prefix="/api/reportes", tags=["Reportes"])

