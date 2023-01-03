# This is the basic functionality required to verify the signature and construct the event from the JSON 
# payload.

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order


@csrf_exempt  #to prevent django from performing a csrf validation
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None 
    
    try:
        event = stripe.Webhook.construct_event(payload, 
                                            sig_header, 
                                            settings.STRIPE_WEBHOOK_SECRET)  #to verify the event signature
        
    except ValueError as e:
        #Invalid payload
        return HttpResponse(status=400)  #Bad request response
    
    except stripe.error.SignatureVerificationError as e:
        #Invalid signature
        return HttpResponse(status=400)
    
    #Implement actions of the webhook endpoint
    if event.type == 'checkout.session.completed':  #We check if checkout is completed
        session = event.data.object  #if we receive the event we retrieve the session object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            #mark order as paid
            order.paid = True
            order.save()
            
    
    return HttpResponse(status=200)  #OK response