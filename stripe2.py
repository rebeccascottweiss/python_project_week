import stripe

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_51HelbYCqbNBsYI2PjoCLV5k87aa7nANj60JnnW9YN0Vpmcgpp7xNT261QkthAKkANXigqE2En5wWc70yHAG7DU8p00qr2fmI1Q'

first_try = stripe.PaymentIntent.create(
    amount=1000,
    currency='usd',
    payment_method_types=['card'],
    receipt_email='jenny.rosen@example.com',
)

print(first_try)