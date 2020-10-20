from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Employee, Bar, Drink, Tab
import bcrypt



def index(request):
    if 'clocked_in' not in request.session:
        request.session['clocked_in'] = []
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
    return redirect ('/bar/employees')


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
    request.session['clocked_in'].append(our_employee)
    return redirect('/bar/dashboard')


def cashout(request):
    employee = Employee.objects.get(id=request.session['employee_id'])
    cash_out = request.session.pop('employee_id')
    request.session['clocked in'].pop(employee)
    return redirect ('/bar')


def dashboard(request):
    if 'employee_id' not in request.session:
        return redirect ('/bar')
    context = {
        'bartender': Employee.objects.get(id = request.session['employee_id']),
        'all_tabs': Tab.objects.all(),
        'all_bartenders': request.session['clocked_in']
    }
    return render (request, 'dashboard.html', context)

def close_out(request, tab_id):
    #payment methodology goes here somewhere. Should there be a rendered html with ways to close out? 
    return redirect('/bar/dashboard')

def drinks(request):
    context = {
        'all_drinks' : Drink.objects.all()
    }
    return render(request, 'drinks.html', context)

def employees(request):
    context = {
        'all_employees' : Employee.objects.all()
    }
    return render (request, 'employees.html', context)

def addemployee(request):
    return render (request, 'addemployee.html')

def adddrink(request):

    return render (request, 'adddrink.html')

def newdrink(request):
    print(request.POST)
    drink = Drink.objects.create(
        name = request.POST['name'],
        description = request.POST['description'],
        cost = request.POST['cost']
    )
    return redirect('/bar/drinks')

def deletedrink(request,number):
    delete_drink = Drink.objects.get(id = number)
    delete_drink.delete()
    return redirect('/bar/drinks')

def edit_tab(request, tab_id):
    context = {
        'bartender': Employee.objects.get(id=request.session['employee_id']), 
        'tab': Tab.objects.get(id=tab_id),
        'drinks': Drink.objects.all(),
    }
    return render(request, 'tabs.html', context)


def delete_drink(request, tab_id, drink_id):
    tab = Tab.objects.get(id=tab_id)
    drink = Drink.objects.get(id=drink_id)
    tab.drinks.remove(drink)
    return redirect(f'/bar/edit/{tab_id}')

def add_order(request, tab_id):
    tab = Tab.objects.get(id=tab_id)
    drink = Drink.objects.get(id=request.POST['drink'])
    tab.drinks.add(drink)
    return redirect(f'/bar/edit/{tab_id}')

def switch_employee(request):
    request.session['employee_id']=request.POST['employee']
    return redirect('/bar/dashboard')
