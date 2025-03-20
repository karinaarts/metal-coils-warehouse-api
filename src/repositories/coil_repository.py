from src.models.coil_model import CoilModel
from src.repositories.base import BaseRepository


class CoilRepository(BaseRepository[CoilModel]):
    def __init__(self):
        super().__init__(CoilModel)
