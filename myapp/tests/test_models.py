from django.db import DataError
from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):
     def test_create_product_with_valid_data(self):
          temp_product = Product.objects.create(name='Temporary product',price = 1.99, available = True)
          self.assertEqual(temp_product.name, 'Temporary product')
          self.assertEqual(temp_product.price, 1.99)
          self.assertTrue(temp_product.available)

     def test_create_product_with_negative_price(self):
          temp_product = Product.objects.create(name='Invalid product', price=-1.99, available=True)
          with self.assertRaises(ValidationError):

               temp_product.full_clean()

     def test_create_product_with_missing_data(self): # Missing price
          temp_product = Product.objects.create(price=1.99, available=True)
          with self.assertRaises(ValidationError):
               temp_product.full_clean()

     def test_create_with_edge_values_price_value(self):# price values
          temp_product = Product.objects.create(name='Temporary product',price=1.999, available=True)
          with self.assertRaises(ValidationError):
               temp_product.full_clean()

     def test_create_with_edge_values_name_length_correct(self):# name length
          temp_product = Product.objects.create(name='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',price=1.99, available=True)
          self.assertEqual(temp_product.name, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
          self.assertEqual(temp_product.price, 1.99)
          self.assertTrue(temp_product.available)


     def test_create_with_edge_values_name_length(self):# name length
          with self.assertRaises(DataError):
               temp_product = Product.objects.create(name='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',price=1.99, available=True)
               temp_product.full_clean()

     def test_create_with_invalid_price_format(self):# name length
          with self.assertRaises(DataError):
               temp_product=Product.objects.create(name='AAAAA',price=1111111111111111111111111.99, available=True)
               temp_product.full_clean()


class CustomerModelTest(TestCase):
     # customer creation with valid data
     def test_create_customer_with_valid_data(self):
          temp_customer = Customer.objects.create(name='Ala',address='Ala ma kota')
          self.assertEqual(temp_customer.name, 'Ala')
          self.assertEqual(temp_customer.address, 'Ala ma kota')

     #missing fields
     def test_create_customer_with_missing_data(self):
          temp_customer = Customer.objects.create( address='Ala ma kota')
          with self.assertRaises(ValidationError):
               temp_customer.full_clean()

     #edge values for name length
     def test_create_customer_with_edge_values(self):
          with self.assertRaises(DataError):
               temp_customer = Customer.objects.create(
                    name='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
                    address='Ala ma kota')
               temp_customer.full_clean()

class OrderModelTests(TestCase):
     def setUp(self):
          self.customer = Customer.objects.create(name='Ala',address='Ala ma kota')
          self.product = Product.objects.create(name='Temporary product',price = 1.99, available = True)
          self.product1 = Product.objects.create(name='product',price = 3.01, available = True)
          self.product2 = Product.objects.create(name='pro duct',price = 3.01, available = False)


     def test_create_order_with_valid_data(self):
          temp_order = Order.objects.create(customer=self.customer, status='New')
          temp_order.products.set([self.product])

          self.assertEqual(temp_order.status, 'New')
          self.assertEqual(temp_order.customer, self.customer)
          self.assertTrue(temp_order.products.filter(id=self.product.id).exists())

     def test_create_order_with_missing_data(self):
          temp_order = Order.objects.create(customer=self.customer, status='')
          temp_order.products.set([self.product])
          with self.assertRaises(ValidationError):
               temp_order.full_clean()

     def test_calculate_price_with_valid_data(self):
          temp_order = Order.objects.create(customer=self.customer, status='New')
          temp_order.products.set([self.product, self.product1])
          price = temp_order.calculate_price()

          expected_price = self.product.price + self.product1.price
          self.assertEqual(price, expected_price)

     def test_calculate_price_with_no_products(self):
          temp_order = Order.objects.create(customer=self.customer, status='New')
          temp_order.products.set([])
          price = temp_order.calculate_price()

          expected_price = 0
          self.assertEqual(price, expected_price)

     def test_check_if_possible_with_valid_data(self):
          temp_order = Order.objects.create(customer=self.customer, status='New')
          temp_order.products.set([self.product, self.product1])

          is_possible = temp_order.check_if_possible()

          self.assertTrue(is_possible)

     def test_check_if_possible_with_unavailable_product(self):
          temp_order = Order.objects.create(customer=self.customer, status='New')
          temp_order.products.set([self.product, self.product2])

          is_possible = temp_order.check_if_possible()

          self.assertFalse(is_possible)
#