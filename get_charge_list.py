import stripe

stripe.api_key = 'sk_test_51HfHFiJs7YlP147G1rg96ffuvMG5hXYqZHU0hzuYWL2jbL3IjYmbGvxOoKhVoUElXz8CD7GvhkvV6pQn8iAs0H7z00NMXmpSh3'


print(stripe.PaymentMethod.list(
    customer="cus_IFz2oWuXPiGNrW",
    type="card",
).data[0].id)