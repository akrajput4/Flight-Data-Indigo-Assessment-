from django.db import models

from UserManagement.managers.model_manager import DefaultManager
from UserManagement.models.domain_model import Status


class CommonFields(models.Model):
    # Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True,
                               blank=True)

    # Managers
    objects = DefaultManager()

    # Meta
    class Meta:
        abstract = True