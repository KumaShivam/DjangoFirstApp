from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Board, Topic, Post
from .forms import NewTopicForm
import requests

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards':boards})

def newHome(request):
    response = requests.get('http://api.ipstack.com/182.71.119.212?access_key=1613319b90acba66f8467a3884894bb8&format=1')
    geodata = response.json()
    return render(request, 'newHome.html',{
        'ip':geodata['ip'],
        'country':geodata['country_name'],
        'latitude':geodata['latitude'],
        'longitude':geodata['longitude']
    })

def myApi(request):
    response = requests.get('http://127.0.0.1:1111/v1/songs/?format=api')
    musicdata = response.json()
    return render(request, 'myApi.html',{
        'title':musicdata['title'],
        'artist':musicdata['artist']
    })

def board_topics(request, pk):
    board=get_object_or_404(Board,pk=pk)
    return render(request, 'topics.html', {'board':board})
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
        )
        return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board':board, 'form':form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk = pk, pk = topic_pk)
    return render(request, 'topic_post.html', {'topic':topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
    
