from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
  path('', views.login_redirect, name='login_url'),
  path('home/', views.home_redirect, name='home_url'),
  path('register/', views.register_redirect, name='register_url'),
  path('logout/',views.logout_redirect,name = 'logout_url'),
  url("profile/",views.render_profile,name="profile"),
  url(r'^service/author/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',views.manage_profile, name='profile_api'),
  url(r'^service/author/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/github$',views.get_github_events, name='github'),
  path('stream/', views.stream_redirect, name='stream_url'),
  path('post/', views.post_redirect, name='post_url'),
  # url(r'^service/author/(?P<author_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/followers$',views.manage_followers, name='followers_api'),
  # https://stackoverflow.com/questions/32950432/django-urls-uuid-not-working/47948076
  path('service/author/<uuid:author_id>/followers/', views.get_followers),
  path('service/author/<uuid:author_id>/followers/<uuid:foreign_author_id>/', views.edit_followers),
]