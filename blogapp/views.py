"""Model to create QuerySets"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm



# Create your views here.
class PostListView(ListView):
    """ListView Class (Class Based Views)"""
    queryset = Post.published.all()

    context_object_name = "posts"
    paginate_by = 3
    template_name = "blogapp/post/list.html"

def post_list(request,tag_slug = None):
    """ListView Function"""
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = object_list.filter(tags__in = [tag])
    paginator = Paginator(object_list,2)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blogapp/post/list.html", {"page":page, "posts":posts, "tag":tag})

def post_detail(request, year, month, day, post):
    """Details View (Function based views)"""
    post = get_object_or_404(Post, slug=post, status = "published", publish__year=year,
    publish__month = month, publish__day=day)
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
    post_tag_ids = post.tags.values_list("id", flat = True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count("tags")).order_by("-same_tags",
     "-publish")[:4]
    return render(request, "blogapp/post/detail.html",{"post":post, "comments":comments,
     "new_comment": new_comment,"comment_form":comment_form, "similar_posts":similar_posts})

# Sharing a post
def post_share(request, post_id):
    """Created to share"""
    post = get_object_or_404(Post, id = post_id, status = "published")
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_d = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{clean_d['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {clean_d['name']}\
                 comments: {clean_d['comment']}"
            send_mail(subject, message, "gyateng94@gmail.com", [clean_d["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, "blogapp/post/share.html",{"post":post, "form":form, "sent":sent})


def post_search(request):
    """Creating the get post search function"""
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity = TrigramSimilarity("title",query),
                ).filter(similarity__gt=0.3).order_by("-similarity")
    return render(request, "blogapp/post/search.html",{
        "form":form,"query":query, "results":results
    })
