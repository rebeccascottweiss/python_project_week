from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patron
from bar_app.models import Tab
import bcrypt

# Create your views here.
def home(request):
    if 'patron_id' not in request.session:
        return render(request, 'patron_login.html')
    return render(request, 'patron_home.html')

def register(request):
    errors = Patron.objects.validate_register(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    current_patron = Patron.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        valid_to_drink = request.POST['valid_to_drink'],
        email_address = request.POST['email_address'],
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['patron_id'] = current_patron.id
    return redirect('/')

def login(request):
    print("POST payload inside login function", request.POST)
    current_patron = Patron.objects.filter(email_address=request.POST['patron_email'])
    errors = Patron.objects.validate_login(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    if current_patron:
        if bcrypt.checkpw(request.POST['patron_password'].encode(), current_patron.first().password.encode()):
            request.session['patron_id'] = current_patron[0].id
        messages.error(request, "This password doesn't match with the email you entered.")
        return('/')
    messages.error(request, "We don't recognize the email you entered.")
    return redirect('/')
    
def start_tab(request):
    # check if patron has payment applications linked?
    # if patron payment send to current tab page
    if not request.session['payment_info_collected']:
        context = {
            'patron': Patron.objects.get(id=request.session['patron_id'])
        }
        return render(request, 'payment_info.html', context)
    return redirect('/patron_tab')

def add_payment(request):
    # add T/F for if payment information is successful
    request.session['payment_info_collected'] = True
    return redirect('/patron_tab')

def patron_tab(request):
    patron = Patron.objects.get(id=request.session['patron_id'])
    tab_total = sum(patron.tab.drinks.all().cost)
    context = {
        'patron': patron,
        'total': tab_total,
    }
    return render(request, 'patron_tab.html', context)


# this function is a placeholder It did not exist and my make migrations was failing
def pay_tab(request):
    return redirect('/patron_tab')

def logout(request):
    request.session.clear()
    return redirect('/')
