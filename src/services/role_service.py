from repositories.role_repository import role_repository, RoleRepository


class RoleService:

    def __init__(self,
                 default_role_repository: RoleRepository = role_repository):
        self._role_repository = default_role_repository

    def get_all(self):
        return self._role_repository.get_all()

    def get_by_id(self, rid: str):
        return self._role_repository.get_by_id(rid)

    def get_name(self, rid: str):
        return self._role_repository.get_name(rid)


role_service = RoleService()
