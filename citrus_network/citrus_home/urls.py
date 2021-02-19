from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('home/', views.home_redirect),
  path('test', views.test_sign_up),
  path('login/', views.login_redirect),
  path('register/', views.register),
]