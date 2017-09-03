from django.conf.urls import url
from . import views

app_name = "register"

urlpatterns = [
    url(r'^logout$', views.Logout, name='logout'),
    url(r'^login$', views.Login, name='login'),
    url(r'^profile', views.Profile, name='profile'),
    url(r'^password', views.ChangePassword, name='changepassword'),
    url(r'^register$', views.Register, name='register'),
]
