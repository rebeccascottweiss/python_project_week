from django.db import models




class Bar(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #bartenders - related name for bartender id
    #tabs - related name for tabs
    #drinks - related name for drinks 

class Drink(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField
    cost = models.IntegerField()
    bar = models.ForeignKey(Bar, related_name='drinks', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
