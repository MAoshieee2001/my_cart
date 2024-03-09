import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.ecommerce.forms import CategoryForm
from core.ecommerce.models import Category

MODULE_NAME = 'Categoria'


class CategoryTemplateViww(TemplateView):
    template_name = 'category/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_categories':
                # Obtenemos los datos que son mandandos a traves de nuestro dataTables
                start = int(request.POST.get('start', 0))
                length = int(request.POST.get('length', 0))
                search_value = request.POST.get('search[value]', '')
                # Obtener los registros de nuestro models
                categories = Category.objects.all()
                if search_value:
                    categories = categories.filter(names__icontains=search_value)
                # Vamos a crear nuestra paginación con Django
                paginator = Paginator(categories, length)
                get_numbers = start // length + 1
                categories_page = paginator.get_page(get_numbers)

                data = {
                    'data': [category.toJSON() | {'position': position} for position, category in enumerate(categories_page, start=start + 1)],
                    'recordsTotal': paginator.count,
                    'recordsFiltered': paginator.count,
                    'draw': int(request.POST.get('draw', 1))
                }
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CategoryTemplateViww, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Categoria'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('ecommerce:category_list')
        context['create_url'] = reverse_lazy('ecommerce:category_create')
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('ecommerce:category_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Creación de Categoria'
        context['entity'] = MODULE_NAME
        context['action'] = 'create'
        context['list_url'] = self.success_url
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('ecommerce:category_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'update':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Edicción de Categoria'
        context['entity'] = MODULE_NAME
        context['action'] = 'update'
        context['list_url'] = self.success_url
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'delete.html'
    success_url = reverse_lazy('ecommerce:category_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                self.object.delete()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Categoria'
        context['entity'] = MODULE_NAME
        context['action'] = 'delete'
        context['list_url'] = self.success_url
        return context
