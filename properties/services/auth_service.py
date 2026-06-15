from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from properties.models import CustomerProfile


class AuthService:

    @staticmethod
    def register(form):

        user = form.save()

        CustomerProfile.objects.create(
            user=user,
            full_name=form.cleaned_data["full_name"],
            phone=form.cleaned_data["phone"],
            city=form.cleaned_data["city"],
        )

        return user

    @staticmethod
    def login(request, username, password):

        return authenticate(
            request,
            username=username,
            password=password,
        )

    @staticmethod
    def logout(request):

        logout(request)