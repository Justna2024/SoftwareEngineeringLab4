from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest


def hello_world(request):
     return HttpResponse("Hello, World!")


@csrf_exempt
def product_list(request):
     if request.method == 'GET':
          products = list(Product.objects.values('id',
                                                 'name', 'price', 'available'))


          return JsonResponse(products, safe=False)
     elif request.method == 'POST':
          data = json.loads(request.body)
          name = data.get('name')
          price = data.get('price')
          product_id = data.get('id')
          available = data.get('available')
          if name == '' or name == None:
               return HttpResponseBadRequest('Name cannot be empty')
          if price == '' or price == None:
               return HttpResponseBadRequest('Price cannot be empty')
          if price <0 :
               return HttpResponseBadRequest('Price cannot be negative')



          product = Product(name=name,
                       price=Decimal(str(price)), available=available)
          product.full_clean()
          product.save()
          return JsonResponse({
               'id': product.id,
               'name': product.name,
               'price': float(product.price),
               'available': product.available
               },
               status = 201
          )
     elif request.method == 'PATCH':
          return HttpResponseBadRequest('Method not allowed')

@csrf_exempt
def product_detail(request, product_id):
     if request.method == 'GET':
          try:
               product = Product.objects.get(id=product_id)

               return JsonResponse({
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'available': product.available
                    })
          except Product.DoesNotExist:
               return HttpResponseNotFound("Product does not exist")
     elif request.method == 'POST':
          return HttpResponseBadRequest('ID cannot be generated')

