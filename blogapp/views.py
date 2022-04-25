from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blogapp/post/list.html"

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list,1)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blogapp/post/list.html", {"page":page, "posts":posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status = "published", publish__year=year, publish__month = month, publish__day=day)
    return render(request, "blogapp/post/detail.html",{"post":post})