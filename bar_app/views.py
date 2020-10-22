from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Employee, Bar, Drink, Tab, LineItem
import bcrypt



def index(request):
    if 'clocked_in' not in request.session:
        request.session['clocked_in'] = []
    context = {
        "all_employees": Employee.objects.all(),
    }    
    return render(request, 'index.html',context)

def register(request):
    print(request.POST['name'])
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
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
    print(employee)
    request.session['employee_id'] = employee.id
    request.session['clocked_in'].append(employee.id)
    print(employee, request.session['clocked_in'])
    return redirect ('/bar/employees')


def login(request):
    errs = Employee.objects.login_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/bar')
    employee_users = Employee.objects.filter(name = request.POST['name'])
    our_employee = employee_users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), our_employee.password.encode()):
        request.session['employee_id'] = our_employee.id
        request.session['clocked_in'].append(our_employee.id)
        return redirect ('/bar/dashboard')
    messages.error(request, 'Password doesnt match whats on file! Try again!')
    return redirect('/bar')

def logout(request):
    request.session.clear()
    return redirect('/bar')


def cashout(request):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    employee = Employee.objects.get(id=request.session['employee_id'])
    cash_out = request.session.pop('employee_id')
    request.session['clocked_in'].remove(employee.id)
    return redirect ('/bar')


def dashboard(request):
    if 'employee_id' not in request.session:
        return redirect ('/bar')
    new_tabs = []
    for tab in Tab.objects.all():
        if not tab.bartender.all():
            new_tabs.append(tab.id)        
    context = {
        'bartender': Employee.objects.get(id = request.session['employee_id']),
        'all_tabs': Tab.objects.exclude(payment_reference = "123456789"),
        'all_employees': Employee.objects.all(),
        'clocked_in': request.session['clocked_in'],
        'new_tabs' : new_tabs,
    }
    return render (request, 'dashboard.html', context)

def close_out(request, tab_id):
if 'employee_id' not in request.session:
        return redirect('/bar')
    this_tab = Tab.objects.get(id=tab_id)
    this_tab.payment_reference = "123456789"
    this_tab.save()
    print(this_tab.payment_reference)
    filtertabs = Tab.objects.filter
    return redirect('/bar/dashboard')

def drinks(request):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    context = {
        'all_drinks' : Drink.objects.all()
    }
    return render(request, 'drinks.html', context)

def employees(request):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    context = {
        'all_employees' : Employee.objects.all()
    }
    return render (request, 'employees.html', context)

def addemployee(request):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    return render (request, 'addemployee.html')

def adddrink(request):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    return render (request, 'adddrink.html')

def newdrink(request):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    print(request.POST)
    drink = Drink.objects.create(
        name = request.POST['name'],
        description = request.POST['description'],
        cost = request.POST['cost']
    )
    return redirect('/bar/drinks')

def removedrink(request,number):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    remove_drink = Drink.objects.get(id = number)
    remove_drink.delete()
    return redirect('/bar/drinks')

def removeemployee(request,number):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    remove_employee = Employee.objects.get(id = number)
    remove_employee.delete()
    return redirect('/bar/employees')

def edit_tab(request, tab_id):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    context = {
        'bartender': Employee.objects.get(id = request.session['employee_id']),
        'all_employees': Employee.objects.all(),
        'clocked_in': request.session['clocked_in'],
        'tab': Tab.objects.get(id=tab_id),
        'drinks': Drink.objects.all(),
    }
    return render(request, 'tabs.html', context)


def delete_drink(request, tab_id, drink_id):
    if Employee.objects.get(id=request.session['employee_id']).is_manager != True:
        return redirect('/dashboard')
    tab = Tab.objects.get(id=tab_id)
    drink = Drink.objects.get(id=drink_id)
    tab.drinks.remove(drink)
    return redirect(f'/bar/edit/{tab_id}')

def add_order(request, tab_id):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    tab = Tab.objects.get(id=tab_id)
    drink = Drink.objects.get(id=request.POST['drink'])
    tab.drinks.add(drink)
    LineItem.objects.create(
        tab=tab,
        name=drink.name,
        cost=drink.cost,
    )
    tab.total += drink.cost
    tab.save()
    print(LineItem.objects.last())
    return redirect(f'/bar/edit/{tab_id}')

def switch_employee(request):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    request.session['employee_id']=request.POST['employee']
    return redirect('/bar/dashboard')

def editdrink(request,number):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    context ={
        'this_drink' : Drink.objects.get(id = number)
    }
    return render (request, 'editdrink.html', context)


def updatedrink(request,number):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    edit_drink = Drink.objects.get(id = number)
    edit_drink.name = request.POST['name']
    edit_drink.description = request.POST ['description']
    edit_drink.cost = request.POST['cost']
    edit_drink.save()
    return redirect ('/bar/drinks')

def pick_up(request, tab_id):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    bartender = Employee.objects.get(id=request.session['employee_id'])
    tab = Tab.objects.get(id=tab_id)
    tab.bartender.add(bartender)
    return redirect('/bar/dashboard')

def drop(request, tab_id):
    if 'employee_id' not in request.session:
        return redirect('/bar')
    bartender = Employee.objects.get(id=request.session['employee_id'])
    tab = Tab.objects.get(id=tab_id)
    tab.bartender.remove(bartender)
    return redirect('/bar/dashboard')

