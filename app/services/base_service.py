from app.repository.base_repository import BaseRepository


class BaseService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository
