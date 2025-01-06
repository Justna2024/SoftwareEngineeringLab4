from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class Product(models.Model):
     id = models.AutoField(primary_key=True)
     name = models.CharField(max_length=255) # here changed to 50
     price = models.DecimalField(max_digits=20, decimal_places=2)
     available = models.BooleanField()

     def clean(self):
          if self.price <= 0:
               raise ValidationError('Price cannot be negative')

class Customer(models.Model):
     id = models.AutoField(primary_key=True)
     name = models.CharField(max_length=100)
     address = models.CharField(max_length=255)

class Order(models.Model):
     STATUS = {
          "New": "New",
          "In Process": "In Process",
          "Sent": "Sent",
          "Completed": "Completed"
     }


     id = models.AutoField(primary_key=True)
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     products = models.ManyToManyField(Product)
     date = models.DateTimeField(auto_now_add=True)
     status = models.CharField(max_length=20, choices=STATUS)

     def calculate_price(self):
          sum =0
          for product in self.products.all():
               price = product.price
               sum += price
          return sum

     def check_if_possible(self):
          for product in self.products.all():
               if not product.available:
                    return False
          return True