from django.db import models
from home_API.models import Area, Units


class Client(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phoneNO = models.PositiveBigIntegerField()
    massageNO = models.PositiveBigIntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"


class SearchFilter(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Area = models.ManyToManyField(Area)
    startBudget = models.FloatField()
    stopBudget = models.FloatField()
    startCarpetArea = models.FloatField()
    stopCarpetArea = models.FloatField()
    possession = models.DateTimeField()
    requirements = models.CharField(max_length=200)
    units = models.ManyToManyField(Units)

    # Add fields for specific search criteria (e.g., location, price range, category, etc.)

    def __str__(self):
        return f"{self.client.fname} {self.client.lname}"


class FollowUp(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    actions = models.CharField(max_length=100)
    date_sent = models.DateTimeField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.fname} {self.client.lname} - {self.date_sent}"


class Feedback(models.Model):
    follow_up = models.ForeignKey(FollowUp, on_delete=models.CASCADE)
    response = models.CharField(max_length=100)
    message = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.follow_up}- Feedback"
