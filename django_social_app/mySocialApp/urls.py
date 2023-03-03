from django.urls import path
from django.conf.urls import include
from .views import dashboard, profile_list,profile ,register,LogOut,Login

app_name = 'mySocialApp'
urlpatterns = [
    path("",dashboard,name="dashboard"),
    path("accounts/",include("django.contrib.auth.urls")),
    path("profile_list/",profile_list,name="profile_list"),
    path("profile/<int:pk>",profile,name="profile"),
    path("register",register,name = "register"),
    path("logout" ,LogOut,name="LogOut"),
    path("login",Login ,name="Login")
]
