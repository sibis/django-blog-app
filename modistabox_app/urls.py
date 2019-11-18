from django.conf.urls import url, include
from modistabox_app.views import list_blogs, create_blog, view_blog, delete_blog, update_blog

urlpatterns = [
    url(r'^create/$', create_blog, name='create'),
    url(r'^list/$', list_blogs, name='list'),
    url(r'^view/$', view_blog, name='view'),
    url(r'^update/$', update_blog, name='update'),
    url(r'^delete/$', delete_blog, name='delete')
]