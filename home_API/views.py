from datetime import datetime
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProjectSerializer, UnitSerializer, ProjectSerializer1, UnitSerializer1, AreaSerializer, \
    UnitsSerializer, GovernmentalAreaSerializer, ProjectsSerializer, ImageSerializer
from .models import Project, Unit, Area, Units, GovernmentalArea, Image


class ProjectList(APIView):

    def get(self, request):
        units = Unit.objects.all()
        serializer = UnitSerializer1(units, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        units = data.pop('units')
        projectSerializer = ProjectSerializer(data=request.data)
        if projectSerializer.is_valid():

            a = projectSerializer.save()
            print(a.id, a.area)
            for unit in units:
                unit['project_id'] = a.id
                unitSerializer = UnitSerializer(data=unit)
                if unitSerializer.is_valid():
                    u = unitSerializer.save()
                    print(u)
                else:
                    print(unitSerializer.errors)
                    return Response(data=unitSerializer.errors, status=400)
                    # print(unitSerializer.errors)
            # projectSerializer.
            return Response(data={}, status=status.HTTP_201_CREATED)
        print(projectSerializer.errors)
        return Response(data=projectSerializer.errors, status=400)


class AreaAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            area = self.get_object(pk)
            serializer = AreaSerializer(area)
            return Response(serializer.data)
        else:
            areas = Area.objects.all().order_by('formatted_version')
            serializer = AreaSerializer(areas, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AreaSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(serializer.data, status=status.HTTP_208_ALREADY_REPORTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        area = self.get_object(pk)
        serializer = AreaSerializer(area, data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except IntegrityError:
            return Response(serializer.data, status=status.HTTP_208_ALREADY_REPORTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        area = self.get_object(pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Area.objects.get(pk=pk)
        except Area.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class OptionsView(APIView):
    def get(self, request):
        units = Units.objects.all()
        governmentalArea = GovernmentalArea.objects.all()
        unitsSerializer = UnitsSerializer(units, many=True)
        governmentalAreaSerializer = GovernmentalAreaSerializer(governmentalArea, many=True)
        responses = {
            "units": unitsSerializer.data,
            "governmentalArea": governmentalAreaSerializer.data,
        }
        return Response(data=responses, status=status.HTTP_200_OK)


class ProjectsView(APIView):
    def get(self, request):
        project = Project.objects.all()
        projectsSerializer = ProjectsSerializer(project, many=True)
        return Response(projectsSerializer.data)


class ProjectView(APIView):
    def get(self, request, pk):
        project = Project.objects.get(id=pk)
        projectSerializer = ProjectSerializer(project)
        data = projectSerializer.data
        unit = Unit.objects.filter(project_id=pk)
        unitSerializer = UnitSerializer(unit, many=True)
        data.update({'units': unitSerializer.data})
        return Response(data)
        # return Response(projectSerializer.data.update({'nameme': 'akshay'}))

    def put(self, request, pk):
        data = request.data
        try:
            project_id = pk
            project = Project.objects.get(pk=project_id)

        except (KeyError, Project.DoesNotExist):
            return Response(data={'error': 'Invalid project id'}, status=status.HTTP_400_BAD_REQUEST)

        projectSerializer = ProjectSerializer(project, data=data)
        if projectSerializer.is_valid():
            try:
                project_id = pk
                units_to_delete = Unit.objects.filter(project_id=project_id)
                if not units_to_delete.exists():
                    print(f'error: No units found with project_id: {project_id}')
                    # return Response(data={'error': f'No units found with project_id: {project_id}'},
                    #                 status=status.HTTP_404_NOT_FOUND)

                units_to_delete.delete()
                print(f'message:Units deleted successfully')
                # return Response(data={'message': 'Units deleted successfully'}, status=status.HTTP_200_OK)
            except KeyError:
                print(f'error: Invalid request. Project ID not provided.')
                # return Response(data={'error': 'Invalid request. Project ID not provided.'},
                #                 status=status.HTTP_400_BAD_REQUEST)

            projectSerializer.save()

            # Process units if included in the request
            if 'units' in data:
                units = data.pop('units')
                for unit in units:
                    unit['project_id'] = project_id
                    unit_id = unit.get('id')
                    if unit_id:
                        try:
                            unit_obj = Unit.objects.get(pk=unit_id)
                        except Unit.DoesNotExist:
                            return Response(data={'error': f'Invalid unit id: {unit_id}'},
                                            status=status.HTTP_400_BAD_REQUEST)
                        unitSerializer = UnitSerializer(unit_obj, data=unit)
                    else:
                        unitSerializer = UnitSerializer(data=unit)

                    if unitSerializer.is_valid():
                        unitSerializer.save()
                    else:
                        return Response(data=unitSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=projectSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Images(APIView):
    def get(self, request):
        a = Image.objects.all()
        b = ImageSerializer(a, many=True)
        return Response(b.data)

    def post(self, request):
        a = ImageSerializer(data=request.data)
        if a.is_valid():
            a.save()
            return Response(a.data, status=status.HTTP_200_OK)
        else:
            return Response(a.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageView(APIView):

    def get(self, request, pk):
        a = Image.objects.get(id=pk)
        b = ImageSerializer(a)
        return Response(b.data)

    def delete(self, request, pk):
        try:
            image = Image.objects.get(id=pk)
            image.delete()
            return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response({"message": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
