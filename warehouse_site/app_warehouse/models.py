from django.db import models
from django.utils import timezone


class Users(models.Model):
    login = models.CharField(max_length=25)
    password = models.CharField(max_length=10)
    role = models.CharField(max_length=10, default="user")


class CardDetails(models.Model):
    number = models.CharField(max_length=13)
    api_key = models.CharField(max_length=60)


class PersonalArea(models.Model):
    user_id_user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Building(models.Model):
    floor_number = models.IntegerField()
    warehouse_size = models.FloatField()
    status_warehouse = models.CharField(max_length=15, default="Not active")
    warehouse_number = models.CharField(max_length=3)
    cost_per_month = models.FloatField()


class Orders(models.Model):
    OrderSum = models.FloatField()
    LeaseStartDate = models.DateField()
    LeaseEndDate = models.DateField()
    personal_area_idpersonal_area = models.ForeignKey(PersonalArea, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=0)
    building_idbuilding = models.ForeignKey(Building, on_delete=models.CASCADE)


class Review(models.Model):
    text_review = models.CharField(max_length=145)
    user_iduser = models.ForeignKey(Users, on_delete=models.CASCADE)
    building_idbuilding = models.ForeignKey(Building, on_delete=models.CASCADE)