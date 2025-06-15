# django_app/modules/v1/sensors/services.py


from .repositories import SensorsRepository


class SensorsService:
    def __init__(self, repository: SensorsRepository):
        self.repository = repository

    def list(self):
        return self.repository.list()

    def create(self, input_data):
        return self.repository.create(input_data)

    def retrieve(self, pk):
        return self.repository.get(pk)

    def update(self, pk, input_data):
        instance = self.repository.get(pk)
        return self.repository.update(instance, input_data)

    def delete(self, pk):
        instance = self.repository.get(pk)
        self.repository.delete(instance)

    def get_instance(self, pk):
        return self.repository.get(pk)
