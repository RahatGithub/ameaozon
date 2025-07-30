from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code', 'payment_method']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }