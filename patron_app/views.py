from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patron
from bar_app.models import Tab
import bcrypt
import stripe
stripe.api_key = "sk_test_51HelbYCqbNBsYI2PjoCLV5k87aa7nANj60JnnW9YN0Vpmcgpp7xNT261QkthAKkANXigqE2En5wWc70yHAG7DU8p00qr2fmI1Q"


def setup_stripe_customer():
    return stripe.Customer.create()

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

    stripe_customer = setup_stripe_customer()
    # print("This is the stripe customre: ",stripe_customer)
    # print("this is the stripe customr_id: ", stripe_customer['id'])

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
    return redirect('/patron/account')


def start_tab(request):
    # check if patron has payment applications linked?
    # if patron payment send to current tab page
    if 'patron_id' not in request.session:
        return redirect('/')
    start=stripe_start()
    print(start)
    request.session['start'] = start
    print(request.session['start'])
    # because it is a class instance we can just do .id
    print(request.session['start'].id)
    # determine what to do with payment id
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
        messages.success(request, "Your password has been updated")
        return redirect('/patron/account')
    messages.error(request, "This password doesn't match with the email you entered.")
    return redirect('/patron/password_update')

def tip_select(request):
    if 'patron_id' not in request.session:
        return redirect('/')
    patron = Patron.objects.get(id=request.session['patron_id'])
    this_tab = patron.tabs.last()
    # print(request.POST)
    print(int(request.POST['tip']))
    this_tab.total = 1
    this_tab.save()
    print(this_tab.total)
    patron.tabs.last().total += patron.tabs.last().total * \
        int(request.POST['tip']) / 100
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


def stripe_start():
    if 'patron_id' not in request.session:
        return redirect('/')
    return_val = stripe.PaymentIntent.create(
        amount=100,
        currency="usd",
        payment_method_types=["card"],
    )
    return return_val


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
