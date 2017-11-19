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
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete
from django.views.generic.base import RedirectView
from blog import views
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('django.contrib.auth.urls')),
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^$', views.index, name='index'),
    url(r'^page/(?P<page>\d+)$', views.index, name='home_page'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/comment/(?P<page>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^reply_to_comment_(?P<comment_pk>\d+)/$', views.reply_to_comment, name='reply_to_comment'),
    # url(r'^register/$', views.register, name='register'),
    url(r'^user/profile/(?P<username>[\w+-@.]+)/$', views.user_profile, name='user_profile'),
    url(r'^user/new_post/$', views.new_post, name='new_post'),
    url(r'^user/edit_post/$', views.edit_post, name='edit_post'),
    url(r'^category/(?P<cate_name>[\w\s]+)/$', views.index, name='category'),
    url(r'^category/(?P<cate_name>[\w\s]+)/page/(?P<page>\d+)/$', views.index, name='category_page'),
    # django认证框架
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    url(r'password-reset/$', password_reset, name='password_reset'),
    url(r'password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'password-reset/complete/$', password_reset_complete, name='password_reset_complete'),
    url(r'register/$', views.register, name='register'),
    #haystack搜索
    url(r'search/', include('haystack.urls')),
    #favicon图标
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]

