from datetime import timedelta

import pandas as pd
from django.shortcuts import render
from django.utils import timezone

from .forms import ProductForm, ClientForm, OrderForm
from .models import Order, Product, Client


# Create your views here.

def client_show(request):
    client_set = Client.objects.all()

    data = {
        'Имя': [client.name for client in client_set],
        'Электронная почта': [client.email for client in client_set],
        'Номер телефона ': [client.phone for client in client_set],
        'Адрес': [client.address for client in client_set],
        'Дата регистрации': [client.registration_date for client in client_set],
    }

    html_table = pd.DataFrame(data).to_html()
    context = {
        'html_table': html_table,
    }

    return render(request, 'all_client.html', context)


def product_show(request):
    product_set = Product.objects.all()

    data = {
        'Название': [product.name for product in product_set],
        'Описание': [product.description for product in product_set],
        'Цена': [product.price for product in product_set],
        'Количество': [product.quantity for product in product_set],
        'Дата добавления': [product.added_date for product in product_set],
    }

    html_table = pd.DataFrame(data).to_html()
    context = {
        'html_table': html_table,
    }

    return render(request, 'all_product.html', context)


def ordered_products(request, client_id):
    today = timezone.now()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    last_year = today - timedelta(days=365)

    orders_last_week = Order.objects.filter(client_id=client_id, order_date__gte=last_week)
    orders_last_month = Order.objects.filter(client_id=client_id, order_date__gte=last_month)
    orders_last_year = Order.objects.filter(client_id=client_id, order_date__gte=last_year)

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
        'html_table': html_table,
        'client_id': client_id,
    }

    return render(request, 'ordered_products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            image = form.cleaned_data.get('image')
            product = Product(name=name, description=description, price=price, quantity=quantity)
            if image:
                product.image = image
            product.save()
            message = 'Продукт сохранен'
        else:
            message = 'Заполните форму'
    else:
        form = ProductForm()
        message = 'Заполните форму'
    return render(request, 'product_form.html', {'form': form, 'message': message})


def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            registration_date = form.cleaned_data['registration_date']
            client = Client(name=name, email=email, phone=phone, address=address, registration_date=registration_date)
            client.save()
            message = 'Клиент сохранен'
        else:
            message = 'Заполните форму'
    else:
        form = ClientForm()
        message = 'Заполните форму'
    return render(request, 'client_form.html', {'form': form, 'message': message})


def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            product = form.cleaned_data['product']
            total_amount = form.cleaned_data['total_amount']
            order_date = form.cleaned_data['order_date']
            order = Order(client=client, product=product, total_amount=total_amount, order_date=order_date)
            order.save()
            message = 'Заказ сохранен'
        else:
            message = 'Заполните форму'
    else:
        form = OrderForm()
        message = 'Заполните форму'
    return render(request, 'order_form.html', {'form': form, 'message': message})
