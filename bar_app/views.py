from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt



def index(request):
    if 'user_id' in request.session:
        return redirect('/welcome')
    context = {
        "all_users": User.objects.all(),
    }
    return render(request, 'index.html',context)

def register(request):
    errs = User.objects.user_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    password = request.POST ['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed
    )
    request.session['user_id'] = user.id
    return redirect ('/welcome')


def login(request):
    print(request.POST['email'])
    errs = User.objects.login_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    email_users = User.objects.filter(email = request.POST['email'])
    our_user = email_users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), our_user.password.encode()):
        request.session['user_id'] = our_user.id
        return redirect ('/')
    messages.error(request, 'Password doesnt match whats on file! Try again!')
    return redirect('/welcome')

def logout(request):
    request.session.clear()
    return redirect ('/')

def welcome(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    context = {
        'logged_in_user': User.objects.get(id = request.session['user_id']),
        'all_users': User.objects.all(),
    }
    return render (request, 'welcome.html',context)