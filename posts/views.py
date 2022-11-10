from email import message

from django.shortcuts import render, redirect
from .models import Post, Ask, Link, Comment, Like
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from itertools import chain
from operator import attrgetter

# Create your views here.
def posts(request): #newest
    asks = Ask.objects.all()#order_by('-created_at')
    links = Link.objects.all()#order_by('-created_at')
    posts = sorted(chain(asks, links), key=attrgetter('created_at'), reverse=True)
    liked_posts=[]
    try:
        liked_posts = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    except:
        pass    
        
    return render(request, 'posts/posts.html',{'posts':posts, 'liked_posts':liked_posts})

def posts_relevant(request):
    asks = Ask.objects.all()#order_by('-likes', '-created_at')
    links = Link.objects.all()#order_by('-likes', '-created_at')
    posts = sorted(chain(asks, links), key=attrgetter('likes'), reverse=True)

    liked_posts=[]
    try:
        liked_posts = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    except:
        pass    
        
    return render(request, 'posts/posts.html',{'posts':posts, 'liked_posts':liked_posts})

def generate_comment_tree(post):
    print("///////////////////////////////////////////////////////////////")
    print("Este es el post:     -> ",post)
    # print("Este es el tree:-------------------> ",comment_tree)

    comments = Comment.objects.filter(commented=post.id)
    print("comentarios del post:-> ",comments)
    if not comments:
        return {}
    comment_tree = dict.fromkeys(comments)
    # comment_tree[post] =  #asigna un diccionario al nodo del tree
    for key, value in comment_tree.items():
        print("llama a generate con:-> ",key)
        comment_tree[key] = generate_comment_tree(key)
        
    return comment_tree



@login_required
#TODO: cuidado habria que poner un try catch
def unic_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commented = post
            comment.user = request.user
            comment.save()
        return redirect('unic_post', post_id=post_id)
    else:
        form=CommentForm()
    
    try:
        liked_posts = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    except:
        pass    
    print("------------Empezamos llamando a generate con [[[[[",post)
    comments2 = generate_comment_tree(post)
    print("/////////////Resultado final/////////////")
    print(comments2)
    # comments = Comment.objects.filter(commented=post.id)
    return render(request, 'posts/unic_post.html',{'post':post, 'comments':comments2, 'form':form, 'liked_posts':liked_posts})

@login_required
def submit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        url = request.POST['url']

        user = User.objects.get(username=request.user.username)
        
        if url =="":
            post = Ask(title=title, content=content, likes=0, user=user)
            post.save()
        else:
            try:
                already_posted = Link.objects.get(url=url)
                if  already_posted:
                    return redirect('unic_post', post_id=already_posted.id)
            except:
                post = Link(title=title, content=content, url=url, likes=0, user=user)
                post.save()
                if content != "":
                    # print(content)
                    comment = Comment(content=content, likes=0, commented=post, user=user)
                    comment.save()  
                    

        messages.success(request," Se ha publicado con éxito")
        return redirect('newest')

    return render(request, 'posts/submit.html',{})

@login_required
def like(request, post_id):

    try:
        post = Post.objects.get(id=post_id)
    except:
        Exception("El post con la id: "+post_id+" no se ha encontrado")
    try:
        like = Like.objects.get(liked_by=request.user,post=post)
        like.post.likes -= 1
        like.post.save()
        like.delete()
    except:
        like = Like.objects.create(liked_by=request.user, post=post)
        like.save()
        like.post.likes += 1
        like.post.save()
    
    return redirect(request.META['HTTP_REFERER'])
    
def ask(request):
    ask = Ask.objects.all()
    liked_posts=[]
    try:
        liked_posts = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    except:
        pass    
        
    return render(request, 'posts/posts.html',{'posts':ask, 'liked_posts':liked_posts})


def userpost(request, username):
    request.session['username'] = request.user.username
    try:
        user = User.objects.get(username=username)
        
        
    except User.DoesNotExist:
        Exception("El usuario no existe")
    asks = Ask.objects.filter(user=user)#order_by('-created_at')
    links = Link.objects.filter(user=user)#order_by('-created_at')
    userpost = chain(asks, links)

    liked_posts=[]
    try:
        liked_posts = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    except:
        pass 
    
    return render(request, 'posts/posts.html', {'posts':userpost, 'liked_posts':liked_posts})

@login_required
def uservoted(request):
    posts = []
    liked_post_ids = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    for id in liked_post_ids:
        posts.append(Post.objects.get(id=id))

    return render(request, 'posts/posts.html', {'posts':posts, 'liked_posts':liked_post_ids})
@login_required
def uservoted_posts(request):
    posts = []
    liked_post_ids = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    for id in liked_post_ids:
        print(id)
        try:
            posts.append(Link.objects.get(id=id))
        except:
            pass
        try:
            posts.append(Ask.objects.get(id=id))
        except:
            pass


    return render(request, 'posts/posts.html', {'posts':posts, 'liked_posts':liked_post_ids})

@login_required
def uservoted_comments(request):
    posts = []
    liked_post_ids = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    for id in liked_post_ids:
        print(id)
        try:
            posts.append(Comment.objects.get(id=id))
        except:
            pass

    return render(request, 'posts/posts.html', {'posts':posts, 'liked_posts':liked_post_ids})

def usercomments(request, username):
    try:
        user = User.objects.get(username=username)
        
        
    except User.DoesNotExist:
        Exception("El usuario no existe")
    
    usercomments=Comment.objects.filter(user=user)

    liked_posts=[]
    try:
        liked_posts = Like.objects.filter(liked_by=request.user).values_list('post', flat=True)
    except:
        pass 
    
    return render(request, 'posts/posts.html', {'posts':usercomments, 'liked_posts':liked_posts})