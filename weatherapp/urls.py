from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('cityerror', views.error_message, name='error-message'),  
]
