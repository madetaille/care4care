from django.conf.urls import patterns, url

from c4c_app import views

urlpatterns = patterns('',
    #url(r'^$', views, name='index'),
    url(r'^jobdetail$', views.JobDetail.as_view(), name='job_detail'),
)