from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)     
    employee_id = models.IntegerField()
    is_manager = models.BooleanField(null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Took out the tips field - Save tips in Session? 
    #because they change and would be reset with each shift? 

class Tab(models.Model):
    patron = models.ForeignKey(User, related_name='tabs', on_delete=models.CASCADE)
    drinks = models.ManyToManyField(Drink, related_name='patron_tabs')
    payment_reference = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Took out "Tab Num" - can be interchangable with ID
    #Took out "Total" - But could add it back in. Do we want the 
    #app to store tab totals for record keeping? 