from django.urls import path
from home.views import *

app_name = 'home'

urlpatterns = [
    path('' ,home_view,name='home')
]