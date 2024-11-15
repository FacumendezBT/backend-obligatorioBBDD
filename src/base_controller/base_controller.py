from config.logger import app_logger as logger
from fastapi import HTTPException, Request
from models.generic_model import GenericModel


class BaseController:
    # Métodos reciben la clase- NO un objeto instanciado
    def get_all(self, model: GenericModel) -> list[dict]:
        try:
            collection = model.get_all()
            return [element.to_dict() for element in collection]
        except Exception as e:
            err = f"Error al obtener {model.table}"
            logger.error(f"{err}: {e}")
            raise HTTPException(status_code=500, detail=err)

    def get_by_primkeys(self, model: GenericModel, primkeys: dict) -> dict:
        err = f"Error al obtener desde {model.table}"
        try:
            element = model.get_row(primkeys)
            if element is None:
                raise HTTPException(status_code=404, detail=err)
            return element.to_dict()
        except HTTPException as http_exc:
            logger.warning(f"HTTP {err}: {http_exc.detail}")
            raise http_exc
        except Exception as e:
            logger.error(f"{err} por claves: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"{err} por claves")

    async def _from_request(
        self, model: GenericModel, request: Request, is_new: bool
    ) -> bool:
        try:
            data = await request.json()
            element = model.from_request(data, is_new)
            success = element.save()
            return success
        except Exception as e:
            logger.error(
                f"Error al crear/actualizar en {model.table}: {e}", exc_info=True
            )
            raise HTTPException(
                status_code=500, detail=f"Error al crear/actualizar en {model.table}"
            )

    async def create_from_request(self, model: GenericModel, request: Request) -> bool:
        return await self._from_request(model, request, True)

    async def update_from_request(self, model: GenericModel, request: Request) -> bool:
        return await self._from_request(model, request, False)

    def delete_from_primkeys(self, model: GenericModel, primkeys: dict) -> bool:
        err = f"Error al obtener desde {model.table}"
        try:
            element = model.get_row(primkeys)
            if element is None:
                raise HTTPException(status_code=404, detail=err)
            success = element.delete_self()
            return success
        except HTTPException as http_exc:
            logger.warning(f"HTTP {err}: {http_exc.detail}")
            raise http_exc
        except Exception as e:
            logger.error(f"{err} por claves: {e}", exc_info=True)
            raise HTTPException(
                status_code=500, detail="Error al eliminar el instructor"
            )
