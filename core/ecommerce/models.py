from django.db import models

from django.forms import model_to_dict

from config import settings


class Category(models.Model):
    names = models.CharField(max_length=144, unique=True, verbose_name='Nombre')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoria')
    names = models.CharField(max_length=144, verbose_name='Nombre')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio')
    imagen = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return f'{self.category} - {self.names}'

    def getImagen(self):
        return f'{settings.MEDIA_URL}{self.imagen}' if self.imagen else f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['names'] = self.names
        item['description'] = self.description
        item['stock'] = self.stock
        item['pvp'] = float(self.pvp)
        item['imagen'] = self.getImagen()
        return item

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
