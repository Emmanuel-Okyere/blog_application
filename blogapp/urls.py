"""URL"""
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from blogapp import views
from blogapp.sitemaps import PostSitemap
from .feeds import LatestPostsFeed
app_name = "blogapp"

sitemaps = {
    "posts":PostSitemap,
}
urlpatterns = [
    path("", views.post_list, name = "post_list"),
    # path("", views.PostListView.as_view(), name = "post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name ="post_detail"),
    path("<int:post_id>/share", views.post_share, name= "post_share"),
    path("tag/<slug:tag_slug>/",views.post_list,name = "post_list_by_tag"),
    path("sitemap.xml", sitemap, {"sitemaps":sitemaps},
    name='django.contrib.sitemaps.views.sitemap'),
    path("feed/",LatestPostsFeed(), name = "post_feed"),
    path("search/" ,views.post_search, name = "post_search")
]
