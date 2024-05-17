from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.config.database_config import get_db
from app.core.exceptions import NotFoundError


class BaseRepository:
    def __init__(self, model: None, db: Session = Depends(get_db)) -> None:
        self.model = model
        self.db = db

    def create(self, schema):
        query = self.model(**schema.dict())
        try:
            self.db.add(query)
            self.db.commit()
            self.db.refresh(query)
            return query
        except IntegrityError as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise e

    def read_all(
        self, eager=False, order_by=None, limit: int = 10, page: int = 1, **filters
    ):
        query = self.db.query(self.model)
        if eager:
            for eager in getattr(self.model, "eagers", []):
                query = query.options(joinedload(getattr(self.model, eager)))

        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)

        if order_by is not None:
            query = query.order_by(order_by)

        return query.limit(limit).offset((page - 1) * limit).all()

    def read_one(self, id: int, eager=False):
        query = self.db.query(self.model)
        if eager:
            for eager in getattr(self.model, "eagers", []):
                query = query.options(joinedload(getattr(self.model, eager)))

        query = query.filter(self.model.id == id).first()
        if not query:
            raise NotFoundError(f"{self.model.__name__} with id {id} not found")
        return query

    def update(self, id: int, schema):
        query = self.read_one(id)
        for key, value in schema.dict().items():
            setattr(query, key, value)
        self.db.commit()
        self.db.refresh(query)
        return query

    def read_where(self, **filters):
        query = self.db.query(self.model)
        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.all()
