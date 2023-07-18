from django.core.management import BaseCommand
from shopapp.models import Product
class Command(BaseCommand):
    """
    Create product
    """
    def handle(self, *args, **options):
        self.stdout.write('Create product')
        products_names = [
            'bmw',
            'toyota',
            'жигули',
        ]
        for products_name in products_names:
            product, create = Product.objects.get_or_create(name=products_name)
            self.stdout.write(f'Create product {product.name}')
        self.stdout.write(self.style.SUCCESS('Products created'))