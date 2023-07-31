from rest_framework import serializers
from .models import Project, Unit, Area, Units, GovernmentalArea


class ProjectSerializer(serializers.ModelSerializer):
    # units = UnitSerializer(many=True)
    class Meta:
        model = Project
        fields = ['area', 'projectName', 'projectType', 'developerName', 'landParcel', 'landmark', 'areaIn',
                  'waterSupply', 'floors', 'flatsPerFloors', 'totalUnit', 'availableUnit', 'amenities', 'parking',
                  'longitude', 'latitude', 'transport', 'readyToMove', 'power', 'goods', 'rera',
                  'possession', 'contactPerson', 'contactNumber', 'marketValue', 'lifts', 'brokerage', 'incentive',
                  ]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['project_id', 'unit', 'CarpetArea', 'price']


class ProjectSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['projectName', 'area', 'rera']


class UnitSerializer1(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    rera = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['project_id', 'project_name', 'area', 'rera', 'unit', 'CarpetArea', 'price', 'longitude', 'latitude',
                  'amenities']

    def get_project_name(self, obj):
        return obj.project_id.projectName

    def get_area(self, obj):
        return obj.project_id.area

    def get_rera(self, obj):
        return obj.project_id.rera

    def get_longitude(self, obj):
        return obj.project_id.longitude

    def get_latitude(self, obj):
        return obj.project_id.latitude

    def get_amenities(self, obj):
        return obj.project_id.amenities


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'


class GovernmentalAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentalArea
        fields = '__all__'
