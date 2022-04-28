"""Generating feeds subscription"""
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    """Getting Latest Post Feeds"""
    title = "My blog"
    link = reverse_lazy("blogapp:post_list")
    description = "New posts of my blog"

    def items(self):
        """Getting Items"""
        return Post.published.all()[:5]

    def items_title(self, item):
        """Getting Item title"""
        return item.title

    def item_description(self, item):
        """Getting Description"""
        return truncatewords(item.body, 30)
