from rest_framework import serializers
from .models import Organization, Employee

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name','email','organization','user_type','locality','assigned_to']

class CreateEmployeeSerializer(serializers.ModelSerializer):
    assigned_to = serializers.UUIDField(source='assigned_to.id', allow_null=True, required=False)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'user_type', 'organization', 'locality', 'assigned_to', 'phone_number','password']

class EmployeeSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source='organization.name', read_only=True)
    assigned_to = serializers.UUIDField(source='assigned_to.id', allow_null=True, required=False)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'user_type', 'organization', 'locality', 'assigned_to', 'phone_number',]
