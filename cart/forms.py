from django import forms
from .models import Order
import re

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Form for adding products to cart or updating quantities"""
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label='Количество'
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class OrderCreateForm(forms.ModelForm):
    """Form for creating an order"""
    agree_to_terms = forms.BooleanField(
        required=True,
        label="Я согласен с условиями обработки персональных данных"
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone',
                  'city', 'shipping_address', 'comment']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'customer_email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email для подтверждения заказа'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактный телефон'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город доставки'}),
            'shipping_address': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Адрес доставки', 'rows': 3}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Дополнительная информация (необязательно)', 'rows': 3}),
        }

    def clean_customer_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('customer_phone')
        if not re.match(r'^\+?\d{10,15}$', phone):
            raise forms.ValidationError('Введите корректный номер телефона.')
        return phone

    def clean_agree_to_terms(self):
        """Ensure user agreed to terms"""
        agree = self.cleaned_data.get('agree_to_terms')
        if not agree:
            raise forms.ValidationError('Вы должны согласиться с условиями обработки персональных данных.')
        return agree