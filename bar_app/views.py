from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Employee, Bar, Drink, Tab
import bcrypt



def index(request):
    if 'employee_id' in request.session:
        return redirect('/bar/dashboard')
    context = {
        "all_employees": Employee.objects.all(),
    }
    return render(request, 'index.html',context)

def register(request):
    errs = Employee.objects.employee_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/bar')
    password = request.POST ['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    employee = Employee.objects.create(
        name = request.POST['name'],
        is_manager = request.POST['is_manager'],
        password = hashed
    )
    request.session['employee_id'] = employee.id
    return redirect ('/bar/dashboard')


def login(request):
    print(request.POST['name'])
    errs = Employee.objects.login_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/bar')
    employee_users = Employee.objects.filter(name = request.POST['name'])
    our_employee = employee_users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), our_employee.password.encode()):
        request.session['employee_id'] = our_employee.id
        return redirect ('/bar')
    messages.error(request, 'Password doesnt match whats on file! Try again!')
    return redirect('/bar/dashboard')


def logout(request):
    request.session.clear()
    return redirect ('/bar')


def dashboard(request):
    if 'employee_id' not in request.session:
        return redirect ('/bar')
    context = {
        'bartender': Employee.objects.get(id = request.session['employee_id']),
    }
    return render (request, 'dashboard.html', context)

def close_out(request, tab_id):
    #payment methodology goes here somewhere. Should there be a rendered html with ways to close out? 
    return redirect('/bar/dashboard')

