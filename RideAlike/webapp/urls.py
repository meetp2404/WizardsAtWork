from django.urls import include, path
from .views import Register, homepage, ulogin,ulogout,upload
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',homepage, name='homepage'),
    path('signup/',Register, name='signup'),
    path('signin/',ulogin,name="signin"),
    path('signout/',ulogout,name="signout"),
    path('upload/',upload,name="upload"),
#     path('loggedin/',loggedin,name="signin"),
#     path('notfound/',notfound,name="signin")
]