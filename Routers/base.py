from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database import Base


class BaseAPI:
    def get_or_404(self, db: Session, model: Type[Base], item_id: int):
        item = db.query(model).filter(model.id == item_id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Eintrag in '{model.__tablename__}' mit ID {item_id} nicht gefunden."
            )

        return item