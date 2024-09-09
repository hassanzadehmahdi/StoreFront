from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TagItem
from store.models import Product


# Register your models here.

class TagItemInLine(GenericTabularInline):
    model = TagItem
    autocomplete_fields = ['tag']
    extra = 0


class CustomProductAdmin(ProductAdmin):
    inlines = [TagItemInLine]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
