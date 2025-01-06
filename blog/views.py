from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Post,
    Like,
    PostView
)
from .forms import (
    PostForm,
    CommentForm,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def post_list(request):
    # qs = Post.objects.all()
    qs = Post.objects.filter(status='p')  
    context = {
        'object_list': qs,
    }
    return render(request, 'blog/post_list.html', context)


@login_required()
def post_create(request):
    
    #! kısa yol
    # form = PostForm(request.POST or None, request.FILES or None) 
    
    #! uzun yol
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # image için FİLES
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")

            return redirect('blog:list')
    context = {
        'form':form
    }
    return render(request, 'blog/post_create.html', context)


def post_detail(request, slug):
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug) # slug=learn-drf-3c78be2186
    
    #! postun görüntülenme istatistiği için;
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=obj)
        # user'ın eğer PostView modelinde objesi varsa getiriyor, yoksa PostView modelinde obje create ediyor.
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = obj
            comment.save()
            return redirect('blog:detail', slug=slug) # best practice.
            # return redirect(request.path) # bu şeklide de yapılabilir.
    context = {
        'object':obj,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context) 
    
    
@login_required()
def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    
    #! url'i yetkisiz userdan koruma 
    if request.user.id != obj.author.id:
        # from django.http import HttpResponse
        # return HttpResponse('You are not authorized!' )
        messages.warning(request, "You're not a writer of this post ")
        return redirect('blog:list')

    if form.is_valid():
        form.save()
        messages.success(request, "Post updated!!")
        return redirect('blog:list')
    context = {
        'object':obj,
        'form': form
    }
    return render(request, 'blog/post_update.html', context)


@login_required() 
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    
    #! url'i yetkisiz userdan koruma
    if request.user.id != obj.author.id:
        # from django.http import HttpResponse
        # return HttpResponse('You are not authorized!' )
        messages.warning(request, "You're not a writer of this post ")
        return redirect('blog:list')
        
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post deleted!!")
        return redirect("blog:list")
    context = {
        "object": obj
    }
    return render(request, "blog/post_delete.html", context)


@login_required()
def like(request, slug):
    if request.method == 'POST':
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        # if like_qs.exists():
        if like_qs:
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)  
        return redirect('blog:detail', slug=slug) # POST için redirect
    return redirect('blog:detail', slug=slug) # GET için redirect