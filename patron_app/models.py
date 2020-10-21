from django.db import models
from datetime import date
import re
# Create your models here.

class Payment(models.Model):
    payment_type = models.CharField(max_length=255) #CC or paypal
    vendor_token = models.CharField(max_length=255) #identification with 3rd party processor
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Identification(models.Model):
    ident_type = models.CharField(max_length=255) # DL or other state ID
    ident_num  = models.CharField(max_length=255) # number on state issued ID
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # dob = models.Date()
    # exp = models.Date()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Validation(models.Manager):
    def validate_register(self, postData):
        errors = {}
        Email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        Name_REGEX = re.compile(r'^[a-zA-Z]+$')
        Password_REGEX = re.compile(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.;:<>?/~_+-=\|])')
        # check to make sure name is longer than 2 chars
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be longer than 2 letters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be longer than 2 letters."
        # add in check to make sure all letters
        if not Name_REGEX.match(postData['first_name']) or not Name_REGEX.match(postData['last_name']):
            errors['first_name_alph'] = "Your name must only contain letters."
        # check if email is valid email format
        if not Email_REGEX.match(postData['email_address']):
            errors['email_address'] = "You must enter a valid email address."
        # check to see if someone already has this email
        for patron in Patron.objects.all():
            if patron.email_address == postData['email_address']:
                errors['dup_email'] = "That email is already registered. Try logging in."
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be 8 or more characters."
        if not Password_REGEX.match(postData['password']):
            errors['pw_chars'] = "Your password must contain: one lowercase letter, one uppercase letter, one number and one special character."
        if postData['password'] != postData['confirm_pw']:
            errors['match_pw'] = "Your passwords must match!"
        # leaving this here to help with age greater than 21 validation
        # if datetime.strptime(postData['b_day'], '%Y-%m-%d') > datetime.now():
        #     errors['b_day'] = "Your birthday must be in the past."
        return errors
        
    def validate_login(self, postData):
        patron = Patron.objects.filter(email_address=postData['patron_email'])
        Email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['patron_password']) < 8:
            errors['password'] = "Your password must be 8 or more characters."
        if not Email_REGEX.match(postData['patron_email']):
            errors['email'] = "You must enter a valid email address."
        return errors

class Patron(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    valid_to_drink = models.BooleanField()
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, default="")
    #identification = models.ForeignKey(Identification, related_name="users", on_delete=models.CASCADE)
    #payments = models.ForeignKey(Payment, related_name="users", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validation()
