from django.db.models.manager import Manager
from django.db.models.query import QuerySet


class BaseManager(Manager):
    # creats and return instance of a model
    def create_model(self, **fields):
        instance = self.model(**fields)
        return self.save(using=self._db)

    # gets the instance of a model
    def get_instance(self, **fields):
        instance = self.get(**fields)
        return instance

    # gets queryset of a model
    def get_querysets(self, **fields):
        queryset = self.get_queryset(**fields)
        return queryset
