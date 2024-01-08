from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        users_info = User.objects.values_list('username', flat=True)
        print(list(users_info))
        for user_info in users_info:
            print(user_info)
        # products_values = Product.objects.values('pk', 'name')
        # for v_product in products_values:
        #     print(v_product)
        self.stdout.write('Dune')