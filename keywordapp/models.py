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
    header = models.TextField(default='')
    date = models.DateField(blank=True)
    content = models.TextField(default='')
    type = models.CharField(default='other',max_length=255)
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header
    
# TempLinkOfHouseModel
class TempLinkOfHouseModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
    
# Page count
class PageCountModel(models.Model):
    count = models.IntegerField()

    def __str__(self):
        return self.count
    
# LinkOfHouseModel
class LinkOfHouseModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
    
# Unwanted Text
class KeywordList(models.Model):
    text = models.TextField(default='')
    type = models.TextField(default='unwanted')

    def __str__(self):
        return self.text
    
# ListOfHouse
class ListOfHouseModel(models.Model):
    header = models.TextField(default='')
    date = models.DateField(blank=True)
    content = models.TextField(default='')
    type = models.CharField(default='other',max_length=255)
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header
    

