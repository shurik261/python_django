from django import forms
from django.core import validators
from django.forms import ModelForm
from django.contrib.auth.models import Group
from .models import Product
# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(
#         label='Description',
#         widget=forms.Textarea(attrs= {'rows': 5, 'cols': 20}),
#         validators=[validators.RegexValidator(
#             regex='great',
#             message='В описании должно быть слово - great'
#         )]
#     )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

