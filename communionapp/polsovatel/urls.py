from django.urls import path
from .views import register,autorisation,home,logout_user,page_user
urlpatterns = [
    path("registrate/", register, name="registrate"),
    path("enter/", autorisation, name="enter"),
    path("", home, name="home"),
    path("logout/", logout_user, name="logout"),
    path("user_page/<str:username>", page_user,name="page_user")
]