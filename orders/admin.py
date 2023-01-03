import csv 
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from . models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')  #the response has to be treated as a csv file
    response['content-Disposition'] = content_disposition  #the httpresponse contains an attached file
    writer = csv.writer(response)  #write to the response obj
    fields = [field for field in opts.get_fields() if not \
        field.many_to_many and not field.one_to_many]  #exclude many-to-many & one-to-many
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    #Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'  #customize the display name
    
def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank>{obj.stripe_id}</a>'
        return mark_safe(html)  #to avoid auto-escaping
    return ''

order_payment.short_description = 'Stripe payment'

#This is a function that takes an Order object as an argument and returns an HTML link for the admin_
#order_detail URL. Django escapes HTML output by default. You have to use the mark_safe function 
#to avoid auto-escaping.

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                        'address', 'postal_code', 'city', 'paid', 
                            order_payment, 'created', 'updated', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]