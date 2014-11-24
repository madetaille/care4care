from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'c4c.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/', include('c4c_app.urls',namespace='c4c')),
    url(r'^admin/', include(admin.site.urls)),
)
