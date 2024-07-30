from django.db import transaction
from rest_framework import serializers
from UserManagement.models.user_model import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_null=True, allow_blank=True, )
    last_name = serializers.CharField(allow_null=True, allow_blank=True)
    email_id = serializers.EmailField()
    password = serializers.CharField(allow_blank=True,allow_null=True)

    @transaction.atomic
    def create(self, validated_data):
        obj = User.objects.create_with_defaults(**validated_data)
        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate(self, attrs):
        return attrs

    class Meta:
        model = User
        fields = '__all__'

