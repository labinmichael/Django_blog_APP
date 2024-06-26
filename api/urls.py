from django.contrib import admin
from django.urls import path
from Register.views import RegisterView,LoginView,LogoutView,UserListView
from home.views import BlogView,BlogSearchView,VisitorBlogView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('blog/',BlogView.as_view()),
    path('blog/search/', BlogSearchView.as_view()),
    path('blog/search/visitors', VisitorBlogView.as_view())
]
