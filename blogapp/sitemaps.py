"""Creating sitemap for SEO"""
from django.contrib.sitemaps import Sitemap
from .models import Post

class  PostSitemap(Sitemap):
    """Creating a sitemap"""
    changefreq = "weekly"
    priority = 0.9


    def items(self):
        '''Getting published Items'''
        return Post.published.all()

    def lastmod(self, obj):
        '''Gettin last modified Items'''
        return obj.updated
