'''Define padrões de URL para users.'''

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # Página de login
    path('', include('django.contrib.auth.urls')),

    # Página de cadastro
    path('register/', views.register, name='register'),

]
