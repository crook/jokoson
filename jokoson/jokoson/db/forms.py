from django import forms
from django.contrib.auth import get_user_model


class UpdateForm(forms.ModelForm):
    class Meta:
        Model = get_user_model()
        fields = ['first_name', 'last_name', 'password', 'email',
                  'user_permissions']
