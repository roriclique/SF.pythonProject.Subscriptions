from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.conf import settings


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
        common_users = Group.objects.get(name="common_users")
        user.groups.add(common_users)
        send_mail(
            subject='Welcome!',
            message=f'{user.username}, you have successfully registered!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user