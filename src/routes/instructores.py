from fastapi import APIRouter
from controller.instructores import get_all_instructores, create_instructor, get_instructor_by_id, update_instructor

base_path = "/instructores"
router = APIRouter()

router.post(base_path)(create_instructor)
router.get(base_path)(get_all_instructores)
router.get(f"{base_path}/{{instructor_id}}")(get_instructor_by_id)
router.put(f"{base_path}/{{instructor_id}}")(update_instructor)
router.delete(f"{base_path}/{{instructor_id}}")(update_instructor)