from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)
    products = [
        Order(**row)
        for row in reader
    ]
    Order.objects.bulk_create(products)
    return products
