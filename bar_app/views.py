from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt



def register(request):
    errs = User.objects.user_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/bar')
    password = request.POST ['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed
    )
    request.session['user_id'] = user.id
    return redirect ('/dashboard')


def login(request):
    print(request.POST['email'])
    errs = User.objects.login_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/bar')
    email_users = User.objects.filter(email = request.POST['email'])
    our_user = email_users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), our_user.password.encode()):
        request.session['user_id'] = our_user.id
        return redirect ('/bar')
    messages.error(request, 'Password doesnt match whats on file! Try again!')
    return redirect('/bar/dashboard')

def logout(request):
    request.session.clear()
    return redirect ('/bar')

def welcome(request):
    if 'user_id' not in request.session:
        return redirect ('/bar')
    context = {
        'bartender': Employee.objects.get(id = request.session['user_id']),
    }
    return render (request, 'welcome.html',context)