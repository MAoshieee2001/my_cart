from django.urls import path

from core.ecommerce.views.category.views import *
from core.ecommerce.views.product.views import *

app_name = 'ecommerce'

urlpatterns = [
    path('category/', CategoryTemplateViww.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('product/', ProductTemplateView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('category/product/', ProductCategoryTemplateView.as_view(), name='product_category_list'),

]
