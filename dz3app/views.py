from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Order, Product

def unique_products_from_orders(orders):
    unique_products = set()
    for order in orders:
        for item in order.orderitem_set.all():
            unique_products.add(item.product)
    return unique_products

def client_orders(request, client_id):
    now = timezone.now()
    client_orders_last_7_days = Order.objects.filter(client_id=client_id, date_ordered__gte=now - timedelta(days=7))
    client_orders_last_month = Order.objects.filter(client_id=client_id, date_ordered__gte=now - timedelta(days=30))
    client_orders_last_year = Order.objects.filter(client_id=client_id, date_ordered__gte=now - timedelta(days=365))

    products_last_7_days = unique_products_from_orders(client_orders_last_7_days)
    products_last_month = unique_products_from_orders(client_orders_last_month)
    products_last_year = unique_products_from_orders(client_orders_last_year)

    context = {
        'products_last_7_days': products_last_7_days,
        'products_last_month': products_last_month,
        'products_last_year': products_last_year,
    }

    return render(request, 'client_products.html', context)