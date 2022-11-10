from django.contrib.auth.models import User
from django import forms

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model= User
        fields = ['username', 'email']
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False