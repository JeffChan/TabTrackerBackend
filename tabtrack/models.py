from django.db import models

# Create your models here.
class User(models.Model):
    facebookID = models.CharField(max_length=50)

class Tab(models.Model):
    #invariant: userID1<userID2
    userID1 = models.IntegerField()
    userID2 = models.IntegerField()
    total = models.IntegerField()
    
class Item(models.Model):
    tabID = models.IntegerField()
    eventID = models.IntegerField()
    description = models.CharField(max_length=200)
    amountCents = models.IntegerField()

class Event(models.Model):
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
