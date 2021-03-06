from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, request

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def check_topic_owner(request, topic):
    '''Verifica se o usuário está associado ao assunto'''
    if topic.owner != request.user:
        raise Http404


def index(request):
    '''A página inicial de learning_log'''
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    '''Mostra todos os tópicos'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    '''Mostra um único assunto e todas as suas entradas.'''
    topic = Topic.objects.get(id=topic_id)

    # Garante que o assunto pertence ao usuário atual
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    '''Adiciona um novo assunto.'''
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos; processa os dados
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    '''Acrescenta uma nova entrada para um assunto em particular.'''
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Nenum dado submetido, cria um formulário em branco
        form = EntryForm()
    else:
        # Dados de POST submentidos; processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Exibe um formuário em branco
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    '''Edita uma entrada existente.'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Protegendo esta página
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Requisição inicial;
        # preenche previamente o formulário com a entrada atual
        form = EntryForm(instance=entry)
    else:
        # Dados de POST submetidos; processa os dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
