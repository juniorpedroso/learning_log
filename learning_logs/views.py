from django.shortcuts import render

# Create your views here.

def index(request):
    '''A página inicial de learning_log'''
    return render(request, 'learning_logs/index.html')

