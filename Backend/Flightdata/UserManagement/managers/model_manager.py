from django.db import models

from UserManagement.models.domain_model import Status


class DefaultManager(models.Manager):
    def create_with_defaults(self, *args, **kwargs):
        return self.create(status=Status.default(), *args, **kwargs)

    def get_api_queryset(self):
        return self.exclude(status=2)


