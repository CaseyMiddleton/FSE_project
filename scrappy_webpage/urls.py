from django.urls import path

from . import views

urlpatterns = [
    path('',views.get_name, name='main'),
    path('integration_test/', views.integration_test),
    path('health/', views.get_health_check, name='health')
]
