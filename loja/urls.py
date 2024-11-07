from django.urls import path
from .views import *     #import all the functions, to run our URL Link from the file views.py   

urlpatterns = [
    path('',homepage, name='homepage' )             #homepage
]