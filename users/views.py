from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    '''Faz o cadastro de um novo usuário.'''
    if request.method != 'POST':
        # Exibe um formulário em branco
        form = UserCreationForm()
    else:
        # Processa o formulário preenchido
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Faz login do usuário e o redireciona para a página inicial
            login(request, new_user)
            return redirect('learning_logs:index')

    # Exibe um formulário inválido ou em branco
    context = {'form': form}
    return render(request, 'registration/register.html', context)
    