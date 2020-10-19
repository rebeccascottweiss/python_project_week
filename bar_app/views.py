from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Employee, Bar, Drink, Tab
import bcrypt



def index(request):
    if 'employee_id' in request.session:
        return redirect('/dashboard')
    context = {
        "all_employees": Employee.objects.all(),
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
    employee = Employee.objects.create(
        name = request.POST['name'],
        is_manager = request.POST['is_manager'],
        password = hashed
    )
    request.session['employee_id'] = employee.id
    return redirect ('/dashboard')


def login(request):
    print(request.POST['name'])
    errs = User.objects.login_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    employee_users = Employee.objects.filter(name = request.POST['name'])
    our_employee = employee_users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), our_employee.password.encode()):
        request.session['employee_id'] = our_employee.id
        return redirect ('/')
    messages.error(request, 'Password doesnt match whats on file! Try again!')
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect ('/')

def welcome(request):
    if 'employee_id' not in request.session:
        return redirect ('/')
    context = {
        'logged_in_employee': Employee.objects.get(id = request.session['employee_id']),
        "all_employees": Employee.objects.all(),
    }
    return render (request, 'dashboard.html', context)