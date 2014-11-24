from django.conf.urls import patterns, url

from c4c_app import views

urlpatterns = patterns('',
    #url(r'^$', views.home, name='home'),
    url(r'^jobdetail/(?P<pk>\d+)/$', views.JobDetail.as_view(), name='job_detail'),
    url(r'^(?P<c4cjob_id>\d+)/acceptjob$', views.acceptJob, name='accept_job'),
    url(r'^(?P<c4cjob_id>\d+)/confirmjob$', views.confirmJob, name='confirm_job'),
    url(r'^userjob/$', views.UserJobs.as_view(), name='user_job'),
    #url(r'^createjob$', views.CreateJob.as_view(), name='create_job'),
)