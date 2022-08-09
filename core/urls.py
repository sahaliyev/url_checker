from django.urls import path
from .views import HomeView, RegisterView, LogoutView, LoginView, UrlsView, check_urls

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home_view"),
    path("register/", RegisterView.as_view(), name="register_view"),
    path("logout/", LogoutView.as_view(), name="logout_view"),
    path("login/", LoginView.as_view(), name="login_view"),
    path("ajax/get_urls/", UrlsView.as_view(), name="urls_view"),
    path("check", check_urls, name="check"),
]
