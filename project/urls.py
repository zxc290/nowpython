"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from blog import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^category/(?P<cate_name>[\w\s]+)/$', views.index, name='category'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
    # all-auth认证框架
    url(r'^accounts/', include('allauth.urls')),
    # url(r'register/$', views.register, name='register'), allauth代替
    # haystack搜索
    url(r'search/', include('haystack.urls')),
    # favicon图标
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    # ajax_comment评论
    url(r'^ajax/comment/$', views.ajax_comment, name='ajax_comment'),
    # django-summernote
    url(r'^summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)