from django.urls import path
from .views import view_normal


urlpatterns = [
    path('', view_normal.test, name='test'),
    path('')
]