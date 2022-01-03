from repositories.type_repository import TypeRepository, type_repository


class TypeService:

    def __init__(self,
                 default_type_repository: TypeRepository = type_repository):
        self._type_repository = default_type_repository

    def new(self, name: str):
        new_type = self._type_repository.new(name)
        return new_type

    def get_all(self):
        types = self._type_repository.get_all()
        return types

    def get_by_id(self, tyid: str):
        type = self._type_repository.get_by_id(tyid)
        return type

    def get_name(self, tyid: str):
        name = self._type_repository.get_name(tyid)
        return name

    def update(self, tyid: str, name: str):
        updated_type = self._type_repository.update(tyid, name)
        return updated_type

    def remove(self, tyid: str):
        self._type_repository.remove(tyid)


type_service = TypeService()
