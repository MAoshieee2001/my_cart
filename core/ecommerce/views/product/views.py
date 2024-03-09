import json
from time import time

from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView

from core.ecommerce.forms import ProductForm, ProductCategoryForm
from core.ecommerce.models import Product, Category

MODULE_NAME = 'Producto'


class ProductTemplateView(TemplateView):
    template_name = 'product/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_products':
                # Parámetros de paginación y búsqueda
                start = int(request.POST.get('start', 0))
                length = int(request.POST.get('length', 10))
                search_value = request.POST.get('search[value]', '')

                print(start)
                print(length)

                print(search_value)

                products = Product.objects.select_related('category')

                # Aplicar búsqueda si se especifica
                if search_value:
                    products = products.filter(Q(names__icontains=search_value) | Q(category__names__icontains=search_value))

                # Paginar los resultados
                paginator = Paginator(products, length)
                print(paginator)
                page_number = start // length + 1
                products_page = paginator.get_page(page_number)
                print(products_page)
                # Preparar datos para respuesta JSON
                data = {
                    'data': [product.toJSON() | {'position': position} for position, product in enumerate(products_page, start=start + 1)],
                    'draw': int(request.POST.get('draw', 1)),
                    'recordsTotal': paginator.count,
                    'recordsFiltered': paginator.count
                }
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super(ProductTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Producto'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('ecommerce:product_list')
        context['create_url'] = reverse_lazy('ecommerce:product_create')
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('ecommerce:product_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_categories':
                term = request.POST.get('term', '').strip()
                categories = Category.objects.all()
                if term:
                    categories = categories.filter(names__icontains=term)
                data = [{'id': category.id, 'text': category.names} for category in categories[:5]]
            elif action == 'create':
                form = self.get_form()
                form.fields['category'].queryset = Category.objects.filter(pk=request.POST['category'])
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opcion.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Creacion de Producto'
        context['entity'] = MODULE_NAME
        context['action'] = 'create'
        context['list_url'] = reverse_lazy('ecommerce:product_list')
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('ecommerce:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ProductUpdateView, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(pk=self.object.category.pk)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_categories':
                term = request.POST.get('term', '').strip()
                categories = Category.objects.all()
                if term:
                    categories = categories.filter(names__icontains=term)
                data = [{'id': category.id, 'text': category.names} for category in categories[:5]]
            elif action == 'update':
                form = self.get_form()
                form.fields['category'].queryset = Category.objects.filter(pk=request.POST['category'])
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opcion.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Actualizacion de Producto'
        context['entity'] = MODULE_NAME
        context['action'] = 'update'
        context['list_url'] = reverse_lazy('ecommerce:product_list')
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'delete.html'
    success_url = reverse_lazy('ecommerce:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                self.object.delete()
            else:
                data['error'] = 'No ha ingresado ninguna opcion.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Actualizacion de Producto'
        context['entity'] = MODULE_NAME
        context['action'] = 'delete'
        context['list_url'] = reverse_lazy('ecommerce:product_list')
        return context


class ProductCategoryTemplateView(FormView):
    form_class = ProductCategoryForm
    template_name = 'product/filter.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_categories':
                term = request.POST.get('term', '').strip()
                categories = Category.objects.all()
                if term:
                    categories = categories.filter(names__icontains=term)
                data = [category.toJSON() | {'text': category.names} for category in categories[:10]]
            elif action == 'get_products_category':
                id_category = int(request.POST['id_category'])
                products = Product.objects.filter(category_id=id_category)
                data = [product.toJSON() for product in products]
            else:
                data['error'] = 'No ha ingresado ninguna opcion.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Ecommerce'
        context['entity'] = MODULE_NAME
        context['products'] = Product.objects.all()
        return context
