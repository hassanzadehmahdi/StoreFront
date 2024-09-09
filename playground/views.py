from django.shortcuts import render
from django.db import transaction
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F, Value, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum

from store.models import Product, Customer, Collection, Order, OrderItem, Cart, CartItem
from tags.models import TagItem


# Create your views here.

# @transaction.atomic
def say_hello(request):
    # products = Product.objects.filter(Q(inventory__lt=20) | ~Q(inventory__gt=10))
    # products = Product.objects.filter(inventory=F('id'))
    # products = Product.objects.order_by('unit_price', '-title')
    # products = Product.objects.earliest('title')
    # products = Product.objects.latest('title')
    # products = Product.objects.last()
    # products = Customer.objects.filter(email__endswith='.com')
    # products = Collection.objects.filter(featured_product__isnull=True)
    # products = Product.objects.filter(inventory__lt=10)
    # products = Order.objects.filter(customer_id=1)
    # products = OrderItem.objects.filter(product__collection_id=3)
    # products = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    # be careful to use. makes a different query for field that is not in the only options
    # products = Product.objects.only('id', 'title')

    # products = Product.objects.defer('description')  # be careful to use. keeps the description to load later

    # products = Order.objects.select_related('customer').prefetch_related(
    #     'orderitem_set__product').order_by('-placed_at')[0:5]

    # products = Order.objects.aggregate(count=Count('id'))
    # products = OrderItem.objects.filter(product_id=1).aggregate(count=Sum('quantity'))
    # products = Order.objects.filter(customer_id=1).aggregate(count=Count('id'))
    # products = Product.objects.filter(collection_id=5).aggregate(min_price=Min('unit_price'),
    #                                                              max_price=Max('unit_price'),
    #                                                              avg_price=Avg('unit_price'),
    #                                                              total_price=Sum('unit_price'))

    # products = Customer.objects.annotate(last_order_id=Max('order__id'))
    # products = Order.objects.filter(customer_id=1)
    # products = Collection.objects.annotate(count=Count('product__id'))
    # products = Customer.objects.annotate(count=Count('order__id')).filter(count__gt=5)
    # products = OrderItem.objects.annotate(total_price=Sum(F('quantity')*F('unit_price')))
    # products = Customer.objects.annotate(total_money_spent=
    #                                      Sum(F('order__orderitem__quantity')*F('order__orderitem__unit_price')))
    # products = Product.objects.annotate(total_sales=
    #                                     Sum(F('orderitem__quantity')*F('orderitem__unit_price')))\
    #                                     .order_by('-total_sales')[:5]
    # products = Product.objects.annotate(value=Value(True))

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # products = Product.objects.annotate(discounted_price=discounted_price)

    # products = TagItem.objects.get_tag_for(Product, 1)

    # Collection.objects.create(title='gemini', featured_product_id=1)
    # Collection.objects.filter(pk=1003).update(featured_product_id=2)
    # Collection.objects.filter(pk=1004).delete()

    # cart = Cart.objects.create()
    # product = Product.objects.get(pk=1)
    # CartItem.objects.create(cart=cart, product=product, quantity=2)

    # CartItem.objects.filter(pk=1).update(quantity=3)

    # Cart.objects.get(pk=1).delete()

    # with transaction.atomic():
    #     order = Order.objects.create(customer_id=1, payment_status='C')
    #     OrderItem.objects.create(order=order, product_id=-1, quantity=2, unit_price=23.3)

    # products = Product.objects.raw('SELECT * from store_product')

    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * from store_product')
    #
    # products = connection.cursor()
    # products.execute('SELECT * from store_product')
    # products.close()

    # with connection.cursor() as cursor:
    #     cursor.callproc('get_customers', [1, 2, 'a'])

    return render(request, 'playground/starting_page.html', {
        'products': list(['products'])
    })

# site for fake data: https://www.mockaroo.com/
