from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patron
from bar_app.models import Tab
import bcrypt
import stripe
# Create your views here.
def home(request):
    if 'patron_id' not in request.session:
        return render(request, 'patron_login.html')
    context = {
        'patron': Patron.objects.get(id=request.session['patron_id'])
    }
    return render(request, 'patron_home.html', context)

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
    current_patron = Patron.objects.filter(email_address=request.POST['patron_email'])
    errors = Patron.objects.validate_login(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    if current_patron:
        if bcrypt.checkpw(request.POST['patron_password'].encode(), current_patron.first().password.encode()):
            request.session['patron_id'] = current_patron.first().id
        messages.error(request, "This password doesn't match with the email you entered.")
        return redirect('/')
    messages.error(request, "We don't recognize the email you entered.")
    return redirect('/')

def update_info(request):
    current_patron = Patron.objects.get(id=request.session['patron_id'])
    # Need to add a new validation field for updating
    current_patron.first_name = request.POST['first_name']
    current_patron.last_name = request.POST['last_name']
    current_patron.email_address = request.POST['email_address']
    current_patron.save()
    return redirect('/patron/account')
    
def start_tab(request):
    # check if patron has payment applications linked?
    # if patron payment send to current tab page
    start=stripe_start()
    print(start)
    request.session['start'] = start
    print(request.session['start'])
    print(request.session['start'].id) #because it is a class instance we can just do .id
    #determine what to do with payment id
    if 'payment_info_collected' not in request.session:
        context = {
            'patron': Patron.objects.get(id=request.session['patron_id'])
        }
        return render(request, 'payment_info.html', context)
    Tab.objects.create(
        patron=Patron.objects.get(id=request.session['patron_id'])
    )
    return redirect('/patron_tab')

def add_payment(request):
    # add T/F for if payment information is successful
    request.session['payment_info_collected'] = True
    #make an instance of a tab for our patron
    Tab.objects.create(
        patron= Patron.objects.get(id=request.session['patron_id'])
    )
    return redirect('/patron_tab')

def patron_tab(request):
    patron = Patron.objects.get(id=request.session['patron_id'])
    # make a total in session to allow for better transfer of data on the backend?
    current_tab = patron.tabs.last()
    if len(current_tab.drinks.all()) > 0:
        current_tab.total = 0
        for drink in current_tab.drinks.all():
            current_tab.total += drink.cost
        current_tab.save()
    context = {
        'patron': patron,
        'current_tab': current_tab,
    }
    return render(request, 'patron_tab.html', context)

#should this come after selecting tip?
def pay_tab(request):
    #process payment info
    #print(stripe_trial)
    return redirect('/tab_receipt')

def tab_receipt(request):
    context = {
        'patron': Patron.objects.get(id=request.session['patron_id']),
    }
    if 'tip' not in request.session:
        return render(request, 'patron_tip.html', context)
    return render(request, 'patron_tab_receipt.html', context)

def account(request):
    context = {
        'patron': Patron.objects.get(id=request.session['patron_id']),
    }
    return render(request, 'patron_account.html', context)

def tip_select(request):
    patron = Patron.objects.get(id=request.session['patron_id'])
    this_tab = patron.tabs.last()
    # print(request.POST)
    print(int(request.POST['tip']))
    this_tab.total = 1
    this_tab.save()
    print(this_tab.total)
    patron.tabs.last().total += patron.tabs.last().total * int(request.POST['tip']) / 100
    request.session['tip'] = True
    return redirect('/tab_receipt')

def return_home(request):
    if 'tip' in request.session:
        del request.session['tip']
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def stripe_start():
    stripe.api_key = "sk_test_51HelbYCqbNBsYI2PjoCLV5k87aa7nANj60JnnW9YN0Vpmcgpp7xNT261QkthAKkANXigqE2En5wWc70yHAG7DU8p00qr2fmI1Q"
    return_val = stripe.PaymentIntent.create(
        amount=100,
        currency="usd",
        payment_method_types=["card"],
    )
    return return_val