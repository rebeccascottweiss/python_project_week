from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def home(request):
    if 'patron_id' not in request.session:
        return render(request, 'patron_login.html')
    return render(request, 'patron_home.html')

def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    current_patron = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        age = request.POST['age'],
        email_address = request.POST['email_address'],
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['patron_id'] = current_patron.id
    return redirect('/')

def login(request):
    current_patron = User.objects.filter(email=request.POST['patron_email'])
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    if current_patron:
        if bcrypt.checkpw(request.POST['patron_password'].encode(), current_patron.first().password.encode()):
            request.session['patron_id'] = current_patron.id
        messages.error(request, "This password doesn't match with the email you entered.")
        return('/')
    messages.error(request, "We don't recognize the email you entered.")
    return redirect('/')
    