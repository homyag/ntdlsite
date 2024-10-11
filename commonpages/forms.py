import re

from django import forms
from .models import CallbackRequest

from django.core.exceptions import ValidationError


class CallbackRequestForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(required=True,
                                        label="Согласие на обработку персональных данных")

    class Meta:
        model = CallbackRequest
        fields = ['name', 'phone', 'agree_to_terms']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш телефон'}),
        }

    def clean_agree_to_terms(self):
        agree_to_terms = self.cleaned_data['agree_to_terms']
        if not agree_to_terms:
            raise forms.ValidationError(
                'Для отправки заявки Вы должны согласиться с условиями '
                'обработки персональных данных.')
        return agree_to_terms

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?\d{10,15}$', phone):
            raise ValidationError('Введите корректный номер телефона.')
        return phone
