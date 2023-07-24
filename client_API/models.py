from django.db import models


class Client(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phoneNO = models.IntegerField()
    massageNO = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class SearchFilter(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Area = models.JSONField()
    startBudget = models.IntegerField()
    stopBudget = models.IntegerField()
    startCarpetArea = models.IntegerField()
    stopCarpetArea = models.IntegerField()
    possession = models.DateTimeField()
    requirements = models.CharField(max_length=200)
    units = models.JSONField()

    # Add fields for specific search criteria (e.g., location, price range, category, etc.)

    def __str__(self):
        return f"{self.client.name}"


class FollowUp(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField()
    actions = models.CharField(max_length=100)
    date_sent = models.DateTimeField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.name} - {self.date_sent}"


class Feedback(models.Model):
    follow_up = models.ForeignKey(FollowUp, on_delete=models.CASCADE)
    response = models.CharField(max_length=100)
    message = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.follow_up}- Feedback"
