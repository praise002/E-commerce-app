from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order
import stripe

# Create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)  # Current order item is retrieved from the db using order session key
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )
        
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',  # Used for one-time-payment
            'client_reference_id': order.id,  #we link stripe payments to orders in our system
            'success_url': success_url,  #Redirect user if payment is successful
            'cancel_url': cancel_url,  #Redirect user to if payment is canceled
            'line_items': []  #We'll populate it with d order items to be purchased
        }
        
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),  #amount in cents and converted to an int
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,  #the number of product to purchase
                }
            )
        
        #Create stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        #Redirect to stripe payment form
        return redirect(session.url, code=303) #redirects the user to stripe
    
    else:
        #It includes order summary and a btn to proceed with the payment
        return render(request, 'payment/process.html', locals())
    
    
def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')