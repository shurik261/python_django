from django.test import TestCase
from shopapp.utils import add_two_number
from django.urls import reverse
from random import choices
from string import ascii_letters
from shopapp.models import Product

class AddTwoNumberTestCase(TestCase):
    def test_add_two_number(self):
        result = add_two_number(2, 3)
        self.assertEquals(result, 5)

class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_product_create_view(self):
        response = self.client.post(
            reverse('shopapp:create_products'),
            {
                'name': self.product_name,
                'price': '123.5',
                'description': 'a good table',
                'discount': '10'

            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )
