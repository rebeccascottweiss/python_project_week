from django.db import models
from patron_app.models import User
import re


class EmployeeManager(models.Manager):
    def employee_validator(self, form_data):
        errors = {}
        if len(form_data['name']) < 2:
            errors['name'] = 'Your name isnt long enough!'
        if len(form_data['password']) < 4:
            errors['password'] = 'Password isnt long enough!'
        if form_data['password'] != form_data ['confirm_password']:
            errors['confirm_password'] = "Passwords dont match! Try again!"
        return errors
    def login_validator(self, form_data):
        errors = {}
        # if not name.match(form_data['name']):    # test whether a field matches the pattern            
        #     errors['name'] = "Invalid Employee"
        if len(form_data['password']) < 4:
            errors['password'] = 'Password isnt long enough!'
        return errors

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
    description = models.TextField(default='')
    cost = models.IntegerField()
    bar = models.ForeignKey(Bar, related_name='drinks', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Employee(models.Model):
    name = models.CharField(max_length=255)     
    is_manager = models.BooleanField(null=True)
    password = models.CharField(max_length=255)
    # bar = models.ForeignKey(Bar, related_name='bartenders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployeeManager()
    #Took out the tips field - Save tips in Session? 
    #because they change and would be reset with each shift? 

class Tab(models.Model):
    patron = models.ForeignKey(User, related_name='tabs', on_delete=models.CASCADE)
    bartender = models.ManyToManyField(Employee, related_name='open_tabs')
    drinks = models.ManyToManyField(Drink, related_name='patron_tabs')
    payment_reference = models.CharField(max_length=500, null=True)
    total = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Took out "Tab Num" - can be interchangable with ID