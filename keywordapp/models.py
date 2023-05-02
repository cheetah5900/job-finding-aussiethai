from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime
    
     
# TempLinkOfWorkModel
class TempLinkOfWorkModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
    
# LinkOfWorkModel
class LinkOfWorkModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
    
# ListOfWork
class ListOfWorkModel(models.Model):
    header = models.CharField(default='',max_length=255)
    date = models.DateField(blank=True)
    content = models.TextField(default='')
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header
    
# TempLinkOfHouseModel
class TempLinkOfHouseModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
    
    
# LinkOfHouseModel
class LinkOfHouseModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
   
    
# ListOfHouse
class ListOfHouseModel(models.Model):
    header = models.CharField(default='',max_length=255)
    date = models.DateField(blank=True)
    content = models.TextField(default='')
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header
    
# Refresh Check
class RefreshCheck(models.Model):
    times = models.IntegerField(default=0)
    date = models.DateField()

    def __str__(self):
        return self.times

