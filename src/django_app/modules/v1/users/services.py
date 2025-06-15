# django_app/modules/v1/users/services.py


from rest_framework.exceptions import ValidationError

from .filters import UsersFilter
from .repositories import UsersRepository


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def list(self, query_params=None):
        queryset = self.repository.list()
        if query_params:
            filterset = UsersFilter(query_params, queryset=queryset)
            if filterset.is_valid():
                queryset = filterset.qs
            else:
                raise ValidationError(filterset.errors)

        return queryset

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
