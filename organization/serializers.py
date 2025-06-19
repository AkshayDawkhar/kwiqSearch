from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Organization, Employee


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'organization', 'user_type', 'locality', 'assigned_to_sel']


class CreateEmployeeSerializer(serializers.ModelSerializer):
    assigned_to = serializers.UUIDField(source='assigned_to_sel.id', allow_null=True, required=False)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'user_type', 'organization', 'locality', 'assigned_to_sel', 'phone_number',
                  'password','is_active']


class EmployeeSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source='organization.name', read_only=True)
    assigned_to = serializers.UUIDField(source='assigned_to_sel.id', allow_null=True, required=False)
    assigned = serializers.SerializerMethodField()  # New field for `assigned`
    editable = serializers.SerializerMethodField()  # New field for `editable`

    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'user_type', 'organization', 'locality', 'assigned_to_sel', 'phone_number',
                  'assigned', 'editable']

    # Method to check if the employee is assigned to the client
    def get_assigned(self, obj):
        client = self.context.get('client')  # Get the client from context
        if client and obj in client.assignees_to.all():
            return True
        return False

    # Method to check if the employee is editable based on hierarchy
    def get_editable(self, obj):
        current_user_type = self.context.get('current_user_type')  # Get the current user's type from context
        if not current_user_type or current_user_type == 'Visitor':  # If current user type is not found or employee is not a visitor
            return False
        user_type_hierarchy = ['CEO', 'Manager', 'LocalityManager', 'VisitorCaller', 'Caller', 'Visitor']
        if obj.user_type == '':  # CEO is not editable
            return True
        try:
            current_user_index = user_type_hierarchy.index(current_user_type)
            employee_user_index = user_type_hierarchy.index(obj.user_type)
            print(obj.email)
            print(obj.user_type)
            # if obj.user_type == '' or obj.user_type is None:  # Editable if the employee is not assigned a user type
            #     return True
            return employee_user_index >= current_user_index  # Editable if the employee is below the current user type
        except ValueError:
            return False  # Default to False if user types are not found


# serializers.py

class LoginSerializer(serializers.Serializer):
    organization_id = serializers.UUIDField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_organization_id(self, value):
        """Ensure the organization_id exists in the Organization model."""
        try:
            organization = Organization.objects.get(id=value)
        except Organization.DoesNotExist:
            raise ValidationError("Organization does not exist.")
        return value

    def validate(self, attrs):
        """Additional validation can go here."""
        email = attrs.get('email')
        organization_id = attrs.get('organization_id')
        try:
            employee = Employee.objects.get(email=email, organization_id=organization_id)
        except Employee.DoesNotExist:
            raise ValidationError("No user found with this email and organization.")
        return attrs
