from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from urllib3 import PoolManager
from bs4 import BeautifulSoup

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def academias(request):
    return HttpResponse(display+'</table>')

gyms=['lea', 'mogilska', 'solvaypark', 'wadowicka', 'krakowska', 'aleksandry', 'plaza', 'zakopianska', 'nastoku', 'bratyslawska']

display='<table style="width:100%"><tr><th>Aula</th><th>Dia</th><th>Hora</th><th>Academia</th></tr>'
def gym_spider(gym):
        global display
        godziny = []
        zajecia = []
        url = 'http://fitnessplatinium.pl/'+gym+'/grafik/'
        source_code = poolmanager.PoolManager()
        plain_text = source_code.urlopen('GET', url)
        soup = BeautifulSoup(plain_text, "lxml")
        dni=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


        for hour in soup.findAll('td', {'class': 'hour'}):
            if hour.contents==[]:
                hour.contents=['']
            godziny.append(hour.contents)
        for n,i in enumerate(godziny):
            if i==['']:
                godziny[n]=godziny[n-1]
        temp=[]
        for a in godziny:
            if isinstance(a, list):
                temp.extend(a)


        for aula in soup.findAll('td', {'class': 'active'}):
            if aula.contents==None:
                aula.contents=[]
            else:
                aula.contents=str(aula.findAll('h6'))[5:-6]
            zajecia.append([aula.contents])

        for c in zajecia:
            if "&amp" in c[0]:
                c[0]=c[0].replace("&amp;","&")
            c.append(dni[zajecia.index(c)%7])
            c.append(str(temp[int(zajecia.index(c)/7)]))
            c.append(gym)
        klasy=[]
        for c in zajecia:
            if c[0]!='':
                klasy.append(c)
        for klasa in klasy:
            display+='<tr>'
            for info in klasa:
                display+='<td style="text-align:center">'+str(info)+'</td>'
            display+='</tr>'

for gym in gyms:
    gym_spider(gym)


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=post_pk)
