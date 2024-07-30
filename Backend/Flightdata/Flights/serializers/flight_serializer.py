from django.db import transaction
from rest_framework import serializers
from Flights.models.flight_model import Flight, FlightSchedule
from UserManagement.models import User


class FlightSerializer(serializers.ModelSerializer):
    flight_id = serializers.CharField(max_length=255, required=True, allow_blank=True)
    airline = serializers.CharField(max_length=255, required=True, allow_blank=True)
    departure_city = serializers.CharField(max_length=255, required=True, allow_blank=True)
    arrival_city = serializers.CharField(max_length=255, required=True, allow_blank=True)
    departure_schedule = serializers.DateTimeField(required=True, allow_null=True)
    arrival_schedule = serializers.DateTimeField(required=True, allow_null=True)
    flight_duration = serializers.CharField(max_length=255, required=True, allow_blank=True)
    seats_available = serializers.JSONField()

    @transaction.atomic
    def create(self, validated_data):
        obj = Flight.objects.create_with_defaults(**validated_data)
        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate(self, attrs):
        return attrs

    class Meta:
        model = Flight
        fields = '__all__'


class FlightScheduleSerializer(serializers.ModelSerializer):
    flight_id = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(), required=False, allow_null=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    seat_number = serializers.CharField(max_length=255, required=False, allow_blank=True)

    @transaction.atomic
    def create(self, validated_data):
        obj = FlightSchedule.objects.create_with_defaults(**validated_data)
        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate(self, attrs):
        return attrs

    class Meta:
        model = FlightSchedule
        fields = '__all__'
