from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError

from .models import Product
from .serializers import ProductSerializer
# Create your views here.


def index(request):
    return render(request, 'store/index.html')


class ProductsPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 100


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('name',)
    pagination_class = ProductsPagination


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product = Product.objects.all()
        return product

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({'price': 'Must be above $0.00'})
        except ValueError:
            raise ValidationError({'price': 'A valid number is required!'})

        return super().create(request, *args, **kwargs)


class ProductUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')

        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('product_data_{}'.format(product_id))

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            product = response.data
            cache.set('product_data_{}'.format(['id']), {
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
            })
        return response
