from django.forms import *

from core.maintenance.models import *


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'names': TextInput(attrs={
                'placeholder': 'Ingrese el nombre.',
            }),
            'description': Textarea(attrs={
                'placeholder': 'Ingrese la descripción.',
                'rows': 4,
                'style': 'resize:none',
            })
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                self.instance.save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, **kwargs):
        super(ProductForm, self).__init__(**kwargs)
        self.fields['category'].queryset = Category.objects.none()

    class Meta:
        model = Product
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                self.instance.save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductCategoryForm(Form):
    category = ModelChoiceField(queryset=Category.objects.none())
