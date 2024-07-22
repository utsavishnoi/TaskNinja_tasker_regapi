# forms.py

from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)
