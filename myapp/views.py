
from .models import Product, Customer, Order
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from rest_framework import viewsets
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer


def hello_world(request):
     return HttpResponse("Hello, World!")


class ProductViewSet(viewsets.ModelViewSet):
     queryset = Product.objects.all()
     serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
     queryset = Customer.objects.all()
     serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
     queryset = Order.objects.all()
     serializer_class = OrderSerializer
