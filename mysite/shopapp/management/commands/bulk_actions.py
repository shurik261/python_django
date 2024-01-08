from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select actions')
        result = Product.objects.filter(
            name__contains='BMV'
        ).update(discount=10)
        print(result)
        # info = [
        #     ('BMV 3', 20000),
        #     ('BMV 5', 25000),
        #     ('BMV 7', 30000),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)
        self.stdout.write('Dune')