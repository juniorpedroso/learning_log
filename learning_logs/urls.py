'''Define padrões de URL para learning_logs.'''

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [

    # Home page
    path('', views.index, name='index'),

    # Mostra todos os assuntos
    path('topics/', views.topics, name='topics'),

    # Página de detalhes para um único assunto
    path('topics/<int:topic_id>/', views.topic, name='topic'),

]
