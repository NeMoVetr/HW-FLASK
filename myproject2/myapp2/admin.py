from django.contrib import admin

from .models import Client, Order, Product


# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'address', 'registration_date']
    list_filter = ['registration_date']
    search_fields = ['name', 'email', 'phone', 'address']
    search_help_text = 'Поиск по полям имя (name), емайл (email), номер телефона (phone), адрес (address)'


@admin.action(description="Сбросить количество в ноль")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'quantity', 'added_date']
    list_filter = ['added_date']
    search_fields = ['name', 'description']
    search_help_text = 'Поиск по полям имя (name), описание (description)'
    actions = [reset_quantity]


class OrderAdmin(admin.ModelAdmin):
    """Список заказов."""

    list_display = ['client', 'total_amount', 'order_date']

    """Отдельный заказ."""
    readonly_fields = ['order_date']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['client'],
            },
        ),
        (
            'Подробности',
            {
                'classes': ['collapse'],
                'description': 'Содержимое заказа и его общая сумма',
                'fields': ['product', 'total_amount'],
            },
        ),
        (
            'Дата заказа',
            {
                'fields': ['order_date'],
            }
        ),
    ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
