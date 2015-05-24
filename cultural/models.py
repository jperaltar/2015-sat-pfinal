from django.db import models
from django.contrib import admin

# Create your models here.

class Activities(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    eventType = models.CharField(max_length=128)
    price = models.CharField(max_length=16)
    time = models.DateTimeField()
    duration = models.CharField(max_length=128)
    longDuration = models.IntegerField()
    description = models.CharField(max_length=256)
    score = models.IntegerField(default=0)

class User_Activity(models.Model):
    user = models.CharField(max_length=32, primary_key=True)
    activity = models.ManyToManyField(Activities, blank=True, null=True)
    title = models.CharField(max_length=32, blank=True)
    description = models.TextField(blank=True)
    colour = models.CharField(max_length=32, blank=True)

class userTime(models.Model):
    time = models.DateTimeField()
    user = models.CharField(max_length=32)
    activityID = models.IntegerField()

class Comment(models.Model):
    user = models.CharField(max_length=32)
    comment = models.TextField()
    activity = models.ForeignKey(Activities)

class lastUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField()

admin.site.register(User_Activity)
admin.site.register(Activities)
