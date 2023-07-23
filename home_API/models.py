from django.db import models


class Project(models.Model):
    area = models.CharField(max_length=100)
    projectName = models.CharField(max_length=100)
    projectType = models.CharField(max_length=100)
    developerName = models.CharField(max_length=100)
    landParcel = models.FloatField()
    landmark = models.CharField(max_length=100)
    areaIn = models.CharField(max_length=100)
    waterSupply = models.CharField(max_length=100)
    floors = models.IntegerField()
    flatsPerFloors = models.IntegerField()
    totalUnit = models.IntegerField()
    availableUnit = models.IntegerField()
    amenities = models.CharField(max_length=100)
    parking = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    transport = models.BooleanField()
    readyToMove = models.BooleanField()
    power = models.BooleanField()
    goods = models.BooleanField()
    rera = models.DateTimeField()
    possession = models.DateTimeField()
    contactPerson = models.CharField(max_length=100)
    contactNumber = models.IntegerField()
    marketValue = models.IntegerField()
    lifts = models.IntegerField()
    brokerage = models.FloatField()
    incentive = models.IntegerField()


class Unit(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='units')
    unit = models.FloatField()
    CarpetArea = models.IntegerField()
    price = models.IntegerField()
