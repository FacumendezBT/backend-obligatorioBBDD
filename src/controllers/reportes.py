from base_controller.base_controller import BaseController
from fastapi import APIRouter, HTTPException
from models.actividad import Actividad
from models.equipamiento import Equipamiento
from models.clase import Clase
from models.alumno_clase import AlumnoClase
from models.alumno import Alumno
from models.turnos import Turnos
from config.logger import app_logger as logger
from typing import List, Dict

router = APIRouter()
controller = BaseController()

@router.get("/ingresos", summary="Actividades que más ingresos generan",
    responses={
        200: {
            "description": "Reporte de actividades con mayores ingresos.",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "descripcion": "Clases de esquí", "total_ingresos": 15000},
                        {"id": 2, "descripcion": "Clases de snowboard", "total_ingresos": 12000}
                    ]
                }
            }
        },
        500: {"description": "Error al generar el reporte de ingresos."}
    }
)
def actividades_mas_ingresos() -> List[Dict]:
    """
    Reporte de actividades que más ingresos generan, sumando el costo de equipamiento.
    """
    try:
        actividades = Actividad.get_all()
        reporte = []
        for actividad in actividades:
            equipamientos = Equipamiento.get_all_with({"id_actividad": actividad.id})
            total_equipamiento = sum(e.costo for e in equipamientos)
            total_ingresos = actividad.costo + total_equipamiento
            reporte.append({
                "id": actividad.id,
                "descripcion": actividad.descripcion,
                "total_ingresos": total_ingresos
            })
        reporte.sort(key=lambda x: x["total_ingresos"], reverse=True)
        return reporte
    except Exception as e:
        err = "Error al generar el reporte de ingresos."
        logger.error(f"{err}: {e}")
        raise HTTPException(status_code=500, detail=err)

@router.get("/mas_alumnos", summary="Actividades con más alumnos",
    responses={
        200: {
            "description": "Reporte de actividades con más alumnos inscritos.",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "descripcion": "Clases de esquí", "total_alumnos": 30},
                        {"id": 2, "descripcion": "Clases de snowboard", "total_alumnos": 25}
                    ]
                }
            }
        },
        500: {"description": "Error al generar el reporte de actividades con más alumnos."}
    }
)
def actividades_mas_alumnos() -> List[Dict]:
    """
    Reporte de actividades con más alumnos inscritos.
    """
    try:
        clases = Clase.get_all()
        actividad_alumnos = {}
        for clase in clases:
            alumnos_clase = AlumnoClase.get_all_with({"id_clase": clase.id})
            if clase.id_actividad in actividad_alumnos:
                actividad_alumnos[clase.id_actividad] += len(alumnos_clase)
            else:
                actividad_alumnos[clase.id_actividad] = len(alumnos_clase)
        
        actividades = Actividad.get_all()
        reporte = []
        for actividad in actividades:
            total_alumnos = actividad_alumnos.get(actividad.id, 0)
            reporte.append({
                "id": actividad.id,
                "descripcion": actividad.descripcion,
                "total_alumnos": total_alumnos
            })
        reporte.sort(key=lambda x: x["total_alumnos"], reverse=True)
        return reporte
    except Exception as e:
        err = "Error al generar el reporte de actividades con más alumnos."
        logger.error(f"{err}: {e}")
        raise HTTPException(status_code=500, detail=err)

@router.get("/turnos_mas_clases", summary="Turnos con más clases dictadas",
    responses={
        200: {
            "description": "Reporte de turnos con más clases dictadas.",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "hora_inicio": "08:00", "hora_fin": "10:00", "total_clases": 20},
                        {"id": 2, "hora_inicio": "10:00", "hora_fin": "12:00", "total_clases": 15}
                    ]
                }
            }
        },
        500: {"description": "Error al generar el reporte de turnos con más clases dictadas."}
    }
)
def turnos_mas_clases() -> List[Dict]:
    """
    Reporte de turnos con más clases dictadas.
    """
    try:
        clases = Clase.get_all()
        turno_clases = {}
        for clase in clases:
            if clase.dictada:
                if clase.id_turno in turno_clases:
                    turno_clases[clase.id_turno] += 1
                else:
                    turno_clases[clase.id_turno] = 1
        
        turnos = Turnos.get_all()
        reporte = []
        for turno in turnos:
            total_clases = turno_clases.get(turno.id, 0)
            reporte.append({
                "id": turno.id,
                "hora_inicio": str(turno.hora_inicio),
                "hora_fin": str(turno.hora_fin),
                "total_clases": total_clases
            })
        reporte.sort(key=lambda x: x["total_clases"], reverse=True)
        return reporte
    except Exception as e:
        err = "Error al generar el reporte de turnos con más clases dictadas."
        logger.error(f"{err}: {e}")
        raise HTTPException(status_code=500, detail=err)
