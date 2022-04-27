"""Importing from other files"""
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()
@register.simple_tag
def total_post():
    """Getting the total published posts"""
    return Post.published.count()

@register.inclusion_tag("blogapp/post/latest_posts.html")
def show_latest_posts(count = 5):
    """Getting latest post on the blog"""
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts":latest_posts}

@register.simple_tag
def get_most_commented_post(count=5):
    """Getting the most commented post"""
    return Post.published.annotate(total_comments = Count("comments")).order_by\
        ("-total_comments")[:count]

@register.filter(name = "markdown")
def markdown_format(text):
    """Creating the custom filter"""
    return mark_safe(markdown.markdown(text))
