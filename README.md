# Building an online shop
## What the app can do:

### What I learned:
* I created a basic e-commerce application. I made a product catalog and built a 
shopping cart using sessions. I implemented a custom context processor to make the cart available 
to all templates and created a form for placing orders. I also learned how to implement asynchronous tasks using Celery and RabbitMQ.

* I integrated the Stripe payment gateway into my project and created a webhook 
endpoint to receive payment notifications. I built a custom administration action to export orders 
to CSV. I also customized the Django administration site using custom views and templates. Finally, 
I learned how to generate PDF files with WeasyPrint and how to attach them to emails.

* I created a coupon system using Django sessions and integrated it with Stripe. I
also built a recommendation engine using Redis to recommend products that are usually purchased 
together.
#### Basic commands
- pipenv install Django~=4.1.0
- pipenv install python-dotenv
- pipenv install Pillow==9.2.0
- pipenv install django-debug-toolbar

- pipenv install celery==5.2.7
- docker pull rabbitmq
- docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 
rabbitmq:management  **start the server with docker**
- celery -A myshop worker -l info
- celery -A myshop worker -l info --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
- pipenv install flower==1.1.0
- celery -A myshop flower  *To launch the flower*
- pipenv install stripe==4.0.2


- docker pull redis
- docker run -it --rm --name redis -p 6379:6379 redis
- docker exec -it redis sh
- redis-cli
- pipenv install redis==4.3.4

- .\stripe login
- .\stripe listen --forward-to localhost:8000/payment/webhook/
*We use this command above to tell Stripe to listen to events and forward them to our local host*

- pipenv install WeasyPrint==56.1
- python manage.py collectstatic
- pipenv install redis==4.3.4
- docker run -it --rm --name redis -p 6379:6379 redis