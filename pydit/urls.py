"""pydit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from linkaggregator.views import PostList, SinglePost, NewPost, NewComment, Login, Logout, Register, VoteView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^home/$', PostList.as_view(), name='home'),
    url(r'^home/new-post/$', NewPost.as_view(), name='new-post'),
    url(r'^post/new-comment/(?P<slug>[-\w]+)/$', NewComment.as_view(), name='new-comment'),
    url(r'^post/vote/(?P<slug>[-\w]+)/(?P<state>[\w])/$', VoteView.as_view(), name='vote' ),
    url(r'^post/(?P<slug>[-\w]+)/$', SinglePost.as_view(), name='post'),
]
