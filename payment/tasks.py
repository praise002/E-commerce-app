from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'praizthecoder@gmail.com', ["order.email"])  # Create an email obj
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})  # Render template into an html variable
    out = BytesIO()  # An in-memeory bytes buffer
    stylesheets = [weasyprint.CSS(
        settings.STATIC_ROOT / 'css/pdf.css'
    )]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach(
        f'order_{order.id}.pdf',
        out.getvalue(),
        'application/pdf'
        )
    # Send e-mail
    email.send()