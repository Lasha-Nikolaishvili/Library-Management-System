from django.urls import path
from library.views import index


app_name = 'library'
urlpatterns = [
    path('', index, name='index'),
    path('register/', index, name='register'),
    path('login/', index, name='login'),
    path('logout/', index, name='logout'),
]
