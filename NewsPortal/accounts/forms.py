from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignUpForm):
    def save(self, request):
        user = super().save(request)
        send_mail(
            subject='Welcome!',
            message=f'{user.username}, you have successfully registered!',
            from_email='example@yandex.ru',
            recipient_list=[user.email],
        )
        return user