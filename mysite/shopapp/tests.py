from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from shopapp.utils import add_two_number
from django.urls import reverse
from random import choices
from string import ascii_letters
from shopapp.models import Product, Order


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

class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name='Best product')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEquals(response.status_code, 200)

    def test_get_product_and_chek_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):
    fixtures = [
        'product_fixture.json',
    ]
    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        self.assertQuerysetEqual(
        qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
        )


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob_test', password='qwerty')
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)
    def test_order_list_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')

    def test_order_list_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'product_fixture.json',
    ]

    def test_get_product_view(self):
        response = self.client.get(reverse('shopapp:products_export'))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data
        )

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='alex', password='qwerty')
        view_order_permissions = Permission.objects.get(codename='view_order',)

        cls.user.user_permissions.add(view_order_permissions)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(user=self.user, delivery_address='Test Address')

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_detail(self):
        response = self.client.get(reverse('shopapp:orders_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)

        order_in_response = response.context['order']
        self.assertEqual(order_in_response.pk, self.order.pk)

class OrdersExportViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob', password='qwerty', is_staff=True)
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)


    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user,
                'products_id': order.products,
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['orders'],
            expected_data
        )