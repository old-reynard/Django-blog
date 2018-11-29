from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from . import views as v

urlpatterns = [
    re_path(r'^$', v.posts_list, name='list'),
    re_path(r'^create/$', v.posts_create),
    re_path(r'^(?P<id>\d+)/$', v.posts_detail, name='detail'),
    re_path(r'^(?P<id>\d+)/edit/$', v.posts_update, name='update'),
    re_path(r'^(?P<id>\d+)/delete/$', v.posts_delete),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)