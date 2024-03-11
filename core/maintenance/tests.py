from time import time

from config import wsgi

# Create your tests here.
from core.maintenance.models import Product

inicio = time()
products = Product.objects.select_related('category')
data = [product.toJSON() | {'position': position} for position, product in enumerate(products, start=1)]
final = time() - inicio
print(data)
print(final)
