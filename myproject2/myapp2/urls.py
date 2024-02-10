from django.urls import path

from .views import ordered_products, add_product, add_order, add_client, client_show, product_show

urlpatterns = [
    path('ordered-products/<int:client_id>/', ordered_products, name='ordered_products'),
    path('add-product', add_product, name='add_product'),
    path('add-order', add_order, name='add_order'),
    path('add-client', add_client, name='add_client'),
    path('client-show', client_show, name='client_show'),
    path('product-show', product_show, name='product_show'),
]
