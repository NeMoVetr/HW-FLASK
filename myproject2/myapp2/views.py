from datetime import timedelta

import pandas as pd
from django.shortcuts import render
from django.utils import timezone

from myproject2.myapp2.models import Order


# Create your views here.

def ordered_products(request):
    today = timezone.now()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    last_year = today - timedelta(days=365)

    orders_last_week = Order.objects.filter(order_date__gte=last_week)
    orders_last_month = Order.objects.filter(order_date__gte=last_month)
    orders_last_year = Order.objects.filter(order_date__gte=last_year)

    products_last_week = set()
    products_last_month = set()
    products_last_year = set()

    for order in orders_last_week:
        products_last_week.update(order.products.all())
    for order in orders_last_month:
        products_last_month.update(order.products.all())
    for order in orders_last_year:
        products_last_year.update(order.products.all())

    data = {
        'За последние 7 дней (неделю)': [product.name for product in products_last_week],
        'За последние 30 дней (месяц)': [product.name for product in products_last_month],
        'За последние 365 дней (год)': [product.name for product in products_last_year]
    }

    html_table = pd.DataFrame(data).to_html()
    context = {
        'html_table': html_table
    }

    return render(request, 'ordered_products.html', context)
