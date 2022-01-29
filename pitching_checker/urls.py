
from django.contrib import admin
from django.urls import path
from pitching_checker import views
from .views import MyView

urlpatterns = [
    path('', views.index),
    # path('/4H', views.transfer_data)
    path('<path:request_sheet>', MyView.as_view())
]
