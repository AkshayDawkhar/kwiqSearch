from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib3 import request
from django.db.models import Case, When

# from setuptools.package_index import user_agent

from .models import Organization, Employee

from .serializers import OrganizationSerializer, CreateEmployeeSerializer, EmployeeSerializer, LoginSerializer


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer



class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = CreateEmployeeSerializer

class EmployeeActiveInActive(APIView):
    def patch(self, request, pk):
        try:
            active_status = request.data.get('is_active', "Null")
            employee = Employee.objects.get(pk=pk)
            if employee.organization != request.user.organization and request.user.user_type != 'CEO':
                return Response({'message': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
            if active_status == "Null":
                return Response({'message': 'Please provide active status'}, status=status.HTTP_400_BAD_REQUEST)
            if active_status not in [True, False]:
                return Response({'message': 'Invalid active status'}, status=status.HTTP_400_BAD_REQUEST)
            employee.is_active = not employee.is_active
            if employee.auth_token:
                employee.auth_token.delete()
            employee.save()
            return Response({'message': 'Employee status updated successfully'}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            print("Employee not found")
            return Response({'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeListByOrganizationAndUserType(generics.ListAPIView):
    serializer_class = CreateEmployeeSerializer

    def get_queryset(self):
        organization = self.kwargs['organization']
        user_type = self.kwargs['user_type']
        return Employee.objects.filter(organization=organization, user_type=user_type)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from .serializers import LoginSerializer
from .models import Employee
from django.contrib.auth.models import User

class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=400)

        organization_id = serializer.validated_data['organization_id']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            employee = Employee.objects.get(email=email, organization_id=organization_id)
        except Employee.DoesNotExist:
            return Response({
                "message": "No user found with this email and organization."
            }, status=404)

        # Authenticate user
        user = authenticate(username=employee.username, password=password)
        if not user:
            return Response({
                "message": "Invalid credentials"
            }, status=401)

        try:
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
        except IntegrityError:
            return Response({
                "message": "Token generation failed, please try again."
            }, status=500)

        login(request, user)
        return Response({
            "message": "Login Successful",
            "token": token.key,
            "user_type": user.user_type
        }, status=200)

class Logout(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []
    def post(self, request):
        # print(request.user.auth_token.delete)
        request.user.auth_token.delete()
        logout(request)

        return Response({'message': 'Logout Success'})

class CreateEmployee(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.user_type not in ['CEO', 'Manager', 'LocalityManager']:
            return Response({'message': 'Permission Denied'}, status=403)

        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        organization = request.user.organization
        user_type = request.data.get('user_type')

        user = Employee.objects.create_user(email=email, password=password, name=name, organization=organization, user_type=user_type)
        return Response({'message': 'Employee Created',
                         'id': user.id,
                         'name': user.name,
                         'email': user.email,
                         'user_type': user.user_type,
                         'organization': user.organization.id,
                         'password': user.password
                         })

class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('id', None)
        if user_id:
            user = Employee.objects.get(id=user_id)
        else:
            user = request.user
        serializer = EmployeeSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = CreateEmployeeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeListByOrganization(generics.ListAPIView):
    serializer_class = CreateEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # organization = self.kwargs['organization']
        organization = self.request.user.organization
        user_order = Case(
            When(user_type='CEO', then=0),
            When(user_type='Manager', then=1),
            When(user_type='LocalityManager', then=2),
            When(user_type='VisitorCaller', then=3),
            When(user_type='Caller', then=4),
            When(user_type='Visitor', then=5),
            default=6,  # This handles any other values that might be in user_type
        )
        return Employee.objects.filter(organization=organization).order_by(user_order)

class EmployeesView(APIView):
    serializer_class = CreateEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['organization'] = request.user.organization.id
        data['password'] = make_password(data.get('password'))
        serializer = CreateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee Created'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeView(APIView):
    serializer_class = CreateEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request,pk):
        if request.user.user_type != 'CEO':
            return Response({'message': 'Permission Denied'}, status=403)
        try:
            employee = Employee.objects.get(id=pk)
            if employee.organization != request.user.organization:
                return Response({'message': 'Permission Denied'}, status=403)
            employee.delete()
            return Response({'message': 'Employee Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({'message': 'Employee Not Found'}, status=status.HTTP_404_NOT_FOUND)
