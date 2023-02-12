from django.urls import path

from . import views

urlpatterns = [
    path('room/<int:id>/', views.index, name='index'),
]