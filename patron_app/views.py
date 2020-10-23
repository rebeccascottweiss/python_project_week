from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patron
from bar_app.models import Tab
import bcrypt
import stripe
stripe.api_key = "sk_test_51HfHFiJs7YlP147G1rg96ffuvMG5hXYqZHU0hzuYWL2jbL3IjYmbGvxOoKhVoUElXz8CD7GvhkvV6pQn8iAs0H7z00NMXmpSh3"




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

    stripe_customer = setup_stripe_customer(request.POST['first_name'], request.POST['last_name'], request.POST['email_address'])
    print("This is the stripe customre: ",stripe_customer)
    print("this is the stripe customr_id: ", stripe_customer['id'])

    current_patron = Patron.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        valid_to_drink = 'True',
        email_address = request.POST['email_address'],
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode(),
        external_id = stripe_customer['id'],
    )
    request.session['patron_id'] = current_patron.id
    return redirect('/')


def login(request):
    current_patron = Patron.objects.filter(
        email_address=request.POST['patron_email'])
    errors = Patron.objects.validate_login(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    if current_patron:
        if bcrypt.checkpw(request.POST['patron_password'].encode(), current_patron.first().password.encode()):
            request.session['patron_id'] = current_patron.first().id
        messages.error(
            request, "This password doesn't match with the email you entered.")
        return redirect('/')
    messages.error(request, "We don't recognize the email you entered.")
    return redirect('/')


def update_info(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    current_patron = Patron.objects.get(id=request.session['patron_id'])
    errors = Patron.objects.validate_update(request.POST, current_patron)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/patron/account')
    current_patron.first_name = request.POST['first_name']
    current_patron.last_name = request.POST['last_name']
    current_patron.email_address = request.POST['email_address']
    current_patron.save()
    messages.success(request, "Your account info has been updated!")
    return redirect('/patron/account')


def start_tab(request):
    # check if patron has payment applications linked?
    # if patron payment send to current tab page
    if 'patron_id' not in request.session:
        return redirect('/')
    current_patron = Patron.objects.get(id=request.session['patron_id']) 
    stripe_client_secret = stripe_start(current_patron.external_id)
    # not sure we need this in session. the secret changes every time you call it and it may be short lived. Also not sure what we use it for except to register a card.
    request.session['stripe_client_secret'] = stripe_client_secret
    print("inside start_tab stripe_client_secret: ",request.session['stripe_client_secret'])
    # because it is a class instance we can just do .id
    # print(request.session['start'].id)
    # determine what to do with payment id
    #when stripe is implemented this can be changed to: if Patron.objects.get(id=request.session).external_id = "": 
    if 'payment_info_collected' not in request.session:
        context = {
            'patron': Patron.objects.get(id=request.session['patron_id']),
            'clientSecret' : stripe_client_secret
        }
        return render(request, 'payment_info.html', context)
    Tab.objects.create(
        patron=Patron.objects.get(id=request.session['patron_id'])
    )
    return redirect('/patron_tab')


def add_payment(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    # add T/F for if payment information is successful
    request.session['payment_info_collected'] = True
    # make an instance of a tab for our patron
    Tab.objects.create(
        patron=Patron.objects.get(id=request.session['patron_id'])
    )
    return redirect('/patron_tab')


def patron_tab(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    patron = Patron.objects.get(id=request.session['patron_id'])
    # make a total in session to allow for better transfer of data on the backend?
    current_tab = patron.tabs.last()
    if len(current_tab.payment_reference) > 0:
        return redirect("/pay_tab")
    context = {
        'patron': patron,
        'current_tab': current_tab,
    }
    return render(request, 'patron_tab.html', context)

# should this come after selecting tip?


def pay_tab(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    #process payment info
    #print(stripe_trial)
    return redirect('/tab_receipt')


def tab_receipt(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    context = {
        'patron': Patron.objects.get(id=request.session['patron_id']),
        'current_tab': Patron.objects.get(id=request.session['patron_id']).tabs.last(),
    }
    if 'tip' not in request.session:
        return render(request, 'patron_tip.html', context)
    return render(request, 'patron_tab_receipt.html', context)


def account(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    context = {
        'patron': Patron.objects.get(id=request.session['patron_id']),
    }
    return render(request, 'patron_account.html', context)

def password_update(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    return render(request, 'password_update.html')

def password_change(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    current_patron = Patron.objects.get(id=request.session['patron_id'])
    #input password verification
    errors = Patron.objects.validate_password_update(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/patron/password_update')
    if bcrypt.checkpw(request.POST['password_old'].encode(), current_patron.password.encode()) and request.POST['password_new'] == request.POST['password_new_conf']:
        current_patron.password = bcrypt.hashpw(request.POST['password_new'].encode(), bcrypt.gensalt()).decode()
        current_patron.save()
        messages.success(request, "Your password has been updated!")
        return redirect('/patron/account')
    messages.error(request, "This password doesn't match with the email you entered.")
    return redirect('/patron/password_update')

def tip_select(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    patron = Patron.objects.get(id=request.session['patron_id'])
    this_tab = patron.tabs.last()
    stripe_customer_id = patron.external_id
    # print(request.POST)
    print(this_tab.total)
    print(request.POST['other_tip'])
    #refactor to make other_tip to tip and use radio buttons
    if request.POST['other_tip'] == "":
        this_tab.total = round(this_tab.total * (1 + int(request.POST['tip'])/100))
        this_tab.save()
    else:
        this_tab.total = round(this_tab.total * (1 + int(request.POST['other_tip']) / 100))
        this_tab.save()
    print(f"after tip: {this_tab.total}")
    pm_id = stripe_payment_method(stripe_customer_id)
    payment_confirmation = stripe_payment(stripe_customer_id, pm_id, this_tab.total)
    request.session['tip'] = True
    return redirect('/tab_receipt')


def return_home(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    if 'tip' in request.session:
        del request.session['tip']
    return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')

def card_wallet(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    current_patron = Patron.objects.get(id=request.session['patron_id'])
    intent = stripe.SetupIntent.create(
        customer=current_patron.external_id
    )
    context = {
        'client_secret': intent.client_secret
    }
    return render(request, 'card_wallet.html', context)

############# Functions ##############
def setup_stripe_customer(first_name, last_name, email):
    name = first_name + last_name
    return_val = stripe.Customer.create(name=name, email=email)
    return return_val

def stripe_start(stripe_customer_id):
    return_val = stripe.SetupIntent.create(
        customer = stripe_customer_id
    )
    # print("stripe_start (stripe.SetupIntent.create) return value: ", return_val)
    print("stripe_start (stripe.SetupIntent.create) client_secret: ", return_val.client_secret)
    print("leaving Stripe start")
    return return_val.client_secret

def stripe_payment_method(stripe_customer_id):
    pm_list = stripe.PaymentMethod.list(
        customer=stripe_customer_id,
        type="card",
    )
    print(f"stripe_payment_method is running: {pm_list.data[0].id}")
    return pm_list.data[0].id

# needs to be completly thought thru NSB
def stripe_payment(customer_id, pm_id, total):
    try:
        return_val = stripe.PaymentIntent.create(
            amount=total,
            currency="usd",
            customer=customer_id,
            payment_method=pm_id,
            #payment_method_types=["card"],
            off_session=True,
            confirm=True,
        )
        print("")
    except stripe.error.CardError as e:
        err = e.error
        print("Code is: %s" % err.code)
        payment_intent_id = err.payment_intent['id']
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    print("stripe_start (stripe.PaymentIntent.create) return value: ", return_val)
    return return_val