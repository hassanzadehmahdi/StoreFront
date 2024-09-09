from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Customer, Product, Address, Cart, CartItem, Collection, Order, OrderItem, Promotion


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('10<', 'Ok')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        else:
            return queryset.filter(inventory__gt=10)


# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'slug']
    # exclude = ['title']
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_filter = ['last_update', InventoryFilter]
    list_per_page = 10
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'Ok' if product.inventory > 10 else 'Low'

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'customer_orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'first_name']

    def customer_orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
        )
        return format_html(f'<a href={url}>Orders</a>')


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    min_num = 1
    max_num = 10
    autocomplete_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer_name', 'payment_status']
    list_select_related = ['customer']
    list_per_page = 10
    autocomplete_fields = ['customer']
    inlines = [OrderItemInLine]

    def customer_name(self, order):
        return order.customer


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 10
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id),
            })
        )

        return format_html(f'<a href={url}>{collection.products_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Promotion)
