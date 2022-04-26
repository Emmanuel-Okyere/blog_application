from email import message
from operator import imod
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()

    context_object_name = "posts"
    paginate_by = 3
    template_name = "blogapp/post/list.html"

def post_list(request,tag_slug = None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = object_list.filter(tags__in = [tag])
    paginator = Paginator(object_list,3)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blogapp/post/list.html", {"page":page, "posts":posts, "tag":tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status = "published", publish__year=year, publish__month = month, publish__day=day)
    comments = post.comments.filter(active = True)
    new_comment = None
    comment_form = CommentForm(data = request.POST)
    if request.method == "POST":
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, "blogapp/post/detail.html",{"post":post, "comments":comments, "new_comment": new_comment,"comment_form":comment_form})


# Sharing a post
def post_share(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = "published")
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']} comments: {cd['comment']}"
            send_mail(subject, message, "gyateng94@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, "blogapp/post/share.html",{"post":post, "form":form, "sent":sent})