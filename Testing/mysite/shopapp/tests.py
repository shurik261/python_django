from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.shortcuts import reverse

from shopapp.models import Order


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='alex', password='qwerty')
        view_order_permissions = Permission.objects.get(codename='view_order', )
        cls.user.user_permissions.add(view_order_permissions)
        cls.user.save()

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
    fixtures = [
        'product_fixture.json',
        'order_fixture.json',
        'user_fixture.json'
    ]

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
                'user_id': order.user.id,
                'products_id': [product.id for product in order.products.all()],
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['orders'],
            expected_data
        )



