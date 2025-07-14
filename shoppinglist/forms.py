# shoppinglist/forms.py

from django import forms
from .models import ShoppingItem

class ShoppingItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ['product', 'quantity', 'unit']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': '1', 'class': 'form-control', 'placeholder': 'Ilość'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'})
        }
