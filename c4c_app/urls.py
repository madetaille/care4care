from django.conf.urls import patterns, url

from c4c_app import views

urlpatterns = patterns('',
    #url(r'^$', views.home, name='home'),
    url(r'^jobdetail/(?P<pk>\d+)/$', views.JobDetail.as_view(), name='job_detail'),
    url(r'^([\d]+)/userjob/$', views.UserJobs.as_view(), name='user_job'),
    #url(r'^createjob$', views.CreateJob.as_view(), name='create_job'),
)