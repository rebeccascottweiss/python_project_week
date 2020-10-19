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

class Employee(models.Model):
    name = models.CharField(max_length=255)     
    employee_id = models.IntegerField()
    is_manager = models.BooleanField(null=True)
    password = models.CharField(max_length=255)
    bar = models.ForeignKey(Bar, related_name='bartenders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Took out the tips field - Save tips in Session? 
    #because they change and would be reset with each shift? 

class Tab(models.Model):
    patron = models.ForeignKey(User, related_name='tabs', on_delete=models.CASCADE)
    drinks = models.ManyToManyField(Drink, related_name='patron_tabs')
    payment_reference = models.CharField(max_length=500, null=True)
    total=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Took out "Tab Num" - can be interchangable with ID
    
