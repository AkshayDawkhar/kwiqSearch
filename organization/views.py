from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib3 import request

# from setuptools.package_index import user_agent

from .models import Organization, Employee

from .serializers import OrganizationSerializer, EmployeeSerializer

class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer



class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



class EmployeeListByOrganizationAndUserType(generics.ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        organization = self.kwargs['organization']
        user_type = self.kwargs['user_type']
        return Employee.objects.filter(organization=organization, user_type=user_type)

class Login(APIView):
    # authenticate_class = Employee
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        organization_id = request.data.get('organization_id')
        email = request.data.get('email')
        password = request.data.get('password')
        print(organization_id, email, password)
        u = Employee.objects.get(email=email, organization_id=organization_id)
        print(u)
        user = authenticate(username=u.username,password=password)
        print(user)
        if user:
            try:
                token = Token.objects.create(user=user)
            except IntegrityError:
                existing_tokens = Token.objects.filter(user=user)
                existing_tokens.delete()
                logout(request)
                token = Token.objects.create(user=user)
            login(request, user)
            return Response({'message': 'Login Success',
                             'token': token.key,
                             'user_type': user.user_type})
        return Response({'message': 'Login Failed'}, status=401)

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
        serializer = EmployeeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeListByOrganization(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # organization = self.kwargs['organization']
        organization = self.request.user.organization
        return Employee.objects.filter(organization=organization)

class EmployeeView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['organization'] = request.user.organization.id
        data['password'] = make_password(data.get('password'))
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)