from repositories.status_repository import StatusRepository, status_repository


class StatusService:

    def __init__(
            self,
            default_status_repository: StatusRepository = status_repository):
        self._status_repository = default_status_repository

    def new(self, name: str):
        new_status = self._status_repository.new(name)
        return new_status

    def get_all(self):
        statuses = self._status_repository.get_all()
        return statuses

    def get_by_id(self, sid: str):
        status = self._status_repository.get_by_id(sid)
        return status

    def get_name(self, sid: str):
        name = self._status_repository.get_name(sid)
        return name

    def update(self, sid: str, name: str):
        updated_status = self._status_repository.update(sid, name)
        return updated_status

    def remove(self, sid: str):
        self._status_repository.remove(sid)


status_service = StatusService()
