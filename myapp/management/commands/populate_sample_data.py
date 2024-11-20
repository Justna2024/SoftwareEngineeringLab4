from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order
class Command(BaseCommand):
     def handle(self, *args, **kwargs):
          Product.objects.all().delete()
          Customer.objects.all().delete()
          Order.objects.all().delete()

          product1 = Product.objects.create(
               name='HooverMax',
               price=190.99,
               available=True
          )
          product2 = Product.objects.create(
               name='Pressure Pro',
               price=230.99,
               available=True
          )
          product3 = Product.objects.create(
               name='Model 60',
               price=140.50,
               available=True
          )
          customer1 = Customer.objects.create(
               name='John Smith',
               address='308 Negro Arroyo Lane'
          )
          customer2 = Customer.objects.create(
               name='Jane Doe',
               address='6353 Juan Tabo'
          )
          customer3 = Customer.objects.create(
               name='Dwayne Miller',
               address='Quiet 6'
          )
          order1 = Order.objects.create(
               customer=customer1,
               status='Sent'
          )
          order1.products.add(product1)

          order2 = Order.objects.create(
               customer=customer2,
               status='In Process'
          )
          order2.products.add(product2)

          order3 = Order.objects.create(
               customer=customer3,
               status='New'
          )
          order3.products.add(product3)

          self.stdout.write("Data created successfully.")