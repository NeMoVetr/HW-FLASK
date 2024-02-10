from django import forms
from .models import Client, Product, Order

class ClientForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    registration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class ProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity = forms.IntegerField()
    image = forms.ImageField()


class OrderForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    order_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
