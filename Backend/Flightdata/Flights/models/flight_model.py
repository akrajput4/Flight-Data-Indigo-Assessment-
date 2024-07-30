import uuid

from Flights.models.common_model import CommonFields
from django.db import models

from UserManagement.managers.model_manager import DefaultManager
from UserManagement.models import User


class Flight(CommonFields):
    id = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    flight_id = models.CharField(max_length=255, null=True, blank=True)
    airline = models.CharField(max_length=255, null=True, blank=True)
    departure_city = models.CharField(max_length=255, null=True, blank=True)
    arrival_city = models.CharField(max_length=255, null=True, blank=True)
    departure_schedule = models.DateTimeField(null=True, blank=True)
    arrival_schedule = models.DateTimeField(null=True, blank=True)
    flight_duration = models.CharField(max_length=255, null=True, blank=True)
    seats_available = models.JSONField()

    objects = DefaultManager()

    class Meta:
        db_table = 'flight_table'
        app_label = 'Flights'


class FlightSchedule(CommonFields):
    id = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    flight_id = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='flight_details')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='user_details')
    seat_number = models.CharField(max_length=255, null=True, blank=True)

    objects = DefaultManager()

    class Meta:
        db_table = 'flight_schedule'
        app_label = 'Flights'
