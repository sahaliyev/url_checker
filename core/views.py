from dataclasses import fields
from django.shortcuts import render, redirect
from django.views import View

from .models import UrlsToMonitor
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import pdb


def check_urls(request):
    urls = UrlsToMonitor.objects.filter(check_needed=True)
    for item in urls:
        url = item.url
        response = requests.get(url)
        if response.status_code == 200:
            item.status = 1
        else:
            item.status = 0
        item.save()


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("core:login_view")


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:home_view")

        form = UserRegisterForm()
        context = dict()
        context["form"] = form
        return render(request, "register.html", context)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data.pop("confirm_password")

            user = User.objects.create_user(**cleaned_data)
            login(request, user)
            return redirect("core:home_view")
        else:
            return render(request, "register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:home_view")
        return render(request, "login.html")

    def post(self, request):
        # pdb.set_trace()
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # redirect url after user logged in
                next_ = request.GET.get("next")
                if next_:
                    return redirect(next_)
                else:
                    return redirect("core:home_view")
            else:
                messages.error(request, """Username and passowrd does not match!""")
        return render(request, "login.html")


class HomeView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        return render(request, "index.html")


class UrlsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        urls = UrlsToMonitor.objects.filter(check_needed=True)
        urls_list = serializers.serialize(
            "json", list(urls), fields=("url", "status", "created_date", "last_checked")
        )

        return JsonResponse(urls_list, safe=False)
