from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProjectSerializer, UnitSerializer, ProjectSerializer1 ,UnitSerializer1
from .models import Project, Unit


class ProjectList(APIView):

    def get(self, request):
        # a = Project.objects.all()
        # projectSerializer = ProjectSerializer(a, many=True)
        # # print(Project.objects.filter(projectName = 'livience Aventa'))
        # # print(Project.objects.get(id = 1))
        # # print(a[1].id)
        # unit = Unit.objects.all()
        # unitSerializer = UnitSerializer(unit, many=True)
        # if unitSerializer.is_valid():
        #     print(unitSerializer.data)
        # else:
        #     print(unitSerializer.errors)
        # return Response(data=projectSerializer.data)
        # project_name = request.GET.get('projectName', '')
        project_name = ''

        # Filter units based on the project name
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
                    return Response(data=unitSerializer.errors, status=400)
                    # print(unitSerializer.errors)
            # projectSerializer.
            return Response(data={})

        return Response(data=projectSerializer.errors, status=400)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import ProjectSerializer
# from rest_framework import status
#
#
# # Create your views here.
# class HomeAPI(APIView):
#     def get(self, request):
#         item_serializer = ItemSerializer(data=request.data)
#         if item_serializer.is_valid():
#             item = item_serializer.save()
#         return Response(data={"area": "Pashan", "projectName": "livience Aventa ", "projectType": "Multiple Wings",
#                               "developerName": "kohenoor, wel worth.bal developers ", "landParcel": 8,
#                               "landmark": "amer serenity", "areaIn": "PMC", "waterSupply": "PMC", "floors": 36,
#                               "flatsPerFloors": 4, "totalUnit": 575, "availableUnit": 235, "amenities": "All Amenities",
#                               "parking": "covered", "location": "", "transport": True, "readyToMove": False,
#                               "power": True, "goods": True, "rera": "2028-12-01T00:00:00.000",
#                               "possession": "2026-12-01T00:00:00.000", "contactPerson": "s kajve", "contactNumber": 0,
#                               "marketValue": 9500, "lifts": 1, "brokerage": 2.0, "incentive": 0, "bhk": 0.0,
#                               "carpetArea": 0,
#                               "price": 0, "units": [{"unit": "3.0", "CarpetArea": "1438", "price": "210"},
#                                                     {"unit": "4.0", "CarpetArea": "1900", "price": "280"},
#                                                     {"unit": "4.5", "CarpetArea": "2200", "price": "320"},
#                                                     {"unit": "5.0", "CarpetArea": "2876", "price": "450"}]})
#
#     def post(self, request):
#         tem_serializer = ItemSerializer(data=request.data)
#         if item_serializer.is_valid():
#             item = item_serializer.save()

# # myapp/views.py
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import Project, Unit
# from .serializers import ProjectSerializer
#
# @api_view(['POST'])
# def create_project_with_units(request):
#     serializer = ProjectSerializer(data=request.data)
#     if serializer.is_valid():
#         project = serializer.save()
#         units_data = request.data.get('units', [])
#         for unit_data in units_data:
#             unit_data['project'] = project.id
#             Unit.objects.create(**unit_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
