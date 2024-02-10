from django.urls import path
from .views import ordered_products

urlpatterns = [
    path('ordered-products/<int:client_id>/', ordered_products, name='ordered_products'),
]