from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product, Collection, OrderItem, Reviews
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination


# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    # filterset_fields = ['collection_id']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = Product.objects.filter(collection_id=collection_id)
    #
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product can not be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection can not be deleted because it includes one or more products.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

#####################################################
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}

# def get_queryset(self):
#     return Product.objects.select_related('collection').all()
#
# def get_serializer_class(self):
#     return ProductSerializer


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product can not be deleted because it is associated with an order item.'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection can not be deleted because it includes one or more products.'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

###################################################
# class CollectionDetail(APIView):
#     def get(self, request, collection_id):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=collection_id)
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, collection_id):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=collection_id)
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, collection_id):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=collection_id)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection can not be deleted because it includes one or more products.'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductDetail(APIView):
#     def get(self, request, product_id):
#         product = get_object_or_404(Product, pk=product_id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, product_id):
#         product = get_object_or_404(Product, pk=product_id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, product_id):
#         product = get_object_or_404(Product, pk=product_id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product can not be deleted because it is associated with an order item.'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionList(APIView):
#     def get(self, request):
#         collections = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(collections, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = CollectionSerializer(request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductList(APIView):
#     def get(self, request) -> Response:
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request) -> Response:
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
