from django.urls import path

from . import views

urlpatterns = [
    path('',views.get_name),
    path('integration_test/', views.integration_test)
]
