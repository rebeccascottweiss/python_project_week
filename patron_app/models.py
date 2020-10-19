from django.db import models

# Create your models here.

class Payment(models.Model):
    payment_type = models.CharField(max_length=255) #CC or paypal
    vendor_id = models.CharField(max_length=255) #identification with 3rd party processor
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Identification(models.Model):
    ident_type = models.CharField(max_length=255) # DL or other state ID
    ident_num  = models.CharField(max_length=255) # number on state issued ID
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.Date()
    exp = models.Date()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    identification = models.ForeignKey(Identification, related_name="users", on_delete=models.CASCADE)
    payments = models.ForeignKey(Payment, related_name="users", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)