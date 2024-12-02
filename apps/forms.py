from django.contrib.auth.hashers import make_password
from django.forms import ModelForm, Form, CharField

from apps.models import User


class RegisterModelForm(ModelForm):
    class Meta:
        model = User
        fields = 'email', 'password'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)


class LoginForm(Form):
    email = CharField(max_length = 254)
    password = CharField(max_length = 254)