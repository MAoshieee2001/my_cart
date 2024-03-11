from django.urls import path

from core.ecommerce.views.product_ecommerce.views import *

app_name = 'ecommerce'

urlpatterns = [
    path('product/', ProductEcommerceTemplateView.as_view(), name='product_ecommerce'),

]
