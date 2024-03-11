import json
import random
from django.db import transaction
from django.db.transaction import atomic

from config import wsgi, settings
from core.maintenance.models import Product, Category


def insert_category():
    url = f'{settings.BASE_DIR}/deploy/json/categories.json'
    with open(url, encoding='utf8') as product_json:
        with transaction.atomic():
            products = json.load(product_json)
            for product in products:
                p = Product()
                p.category = Category.objects.get_or_create(names=product['names'])[0]
                p.names = product['names']
                p.stock = random.randint(1, 200)
                p.pvp = round(random.randint(1, 100) * random.random(), 2)
                p.save()


insert_category()
