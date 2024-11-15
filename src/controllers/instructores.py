from base_controller.base_controller import BaseController
from config.logger import app_logger as logger
from fastapi import APIRouter, HTTPException, Request
from models.instructor import Instructor

router = APIRouter()
controller = BaseController()


@router.get("/")
def get_all_instructores() -> list[dict]:
    return controller.get_all(Instructor)


@router.get("/{ci}")
def get_instructor_by_id(ci: int) -> dict:
    return controller.get_by_primkeys(Instructor, {"ci": ci})


@router.post("/")
async def create_instructor(request: Request) -> bool:
    return await controller.create_from_request(Instructor, request)


@router.put("/")
async def update_instructor(request: Request) -> bool:
    return await controller.update_from_request(Instructor, request)


@router.delete("/{ci}")
def delete_instructor(ci: int) -> bool:
    return controller.delete_from_primkeys(Instructor, {"ci": ci})
