import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.maintenance.logic.my_cart import Cart
from core.maintenance.models import Product


class ProductEcommerceTemplateView(TemplateView):
    # form_class = ProductCategoryForm
    template_name = 'product_ecommerce/ecommerce.html'
    queryset = Product.objects.all()

    # paginate_by = 20

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_products':
                # Capturamos nuesstros datos
                start = int(request.POST.get('start', 0))
                length = int(request.POST.get('length', 10))
                # LLamamos a nuestro paginator
                paginator = Paginator(self.queryset, length)
                page_number = start // length + 1
                products_page = paginator.get_page(page_number)
                # Obtenemos la paginacion num y el diccionario a mandar
                previous_page = products_page.previous_page_number() if products_page.has_previous() else None
                next_page = products_page.next_page_number() if products_page.has_next() else None
                data = {
                    'products': [product.toJSON() for product in products_page],
                    'previous': previous_page,
                    'next': next_page,
                }
            elif action == 'add_cart':
                id_product = int(request.POST['product_id'])
                product = Product.objects.get(pk=id_product).toJSON()
                product['quantity'] = 1
                product['subtotal'] = 0.00
                # LLamamos a nuestra clase Cart
                cart = Cart(request.session)
                cart.insert_item(product)
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ProductEcommerceTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Ecommerce'
        return context
