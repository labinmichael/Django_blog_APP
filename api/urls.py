from django.contrib import admin
from django.urls import path
from Register.views import RegisterView,LoginView
from home.views import BlogView,BlogSearchView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('blog/',BlogView.as_view()),
    path('blog/search/', BlogSearchView.as_view())
]
