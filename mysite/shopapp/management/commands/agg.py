from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Max, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo aggregate')
        # result = Product.objects.filter(
        #     name__contains='BMV'
        # ).aggregate(
        #     Avg('price'),
        #     Max('price'),
        #     price_min=Min('price'),
        #     count=Count('id'),
        # )
        # print(result)
        orders = Order.objects.annotate(
            total=Sum('products__price'),
            products_count=Count('products'),
        )
        for order in orders:
            print(
                f'Order # {order.id} '
                f'with {order.products_count} '
                f'products worth {order.total}'
            )
        self.stdout.write('Dune')