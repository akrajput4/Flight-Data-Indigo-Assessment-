import uuid
from django.db import models

from UserManagement.managers.model_manager import DefaultManager
from UserManagement.models.common_model import CommonFields


class User(CommonFields):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email_id = models.EmailField()
    password = models.CharField(max_length=255, null=True, blank=True)

    objects = DefaultManager()

    class Meta:
        db_table = 'user_table'
        app_label = 'UserManagement'
