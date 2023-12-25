from django.contrib.auth.models import UserManager


class BaseAuthManager(UserManager):
    def _save(self, **fields):
        instance = self.model(**fields)
        instance.save(using=self._db)
        return instance
