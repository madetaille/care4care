from django.conf.urls import patterns, url

from c4c_app import views

urlpatterns = patterns('',
    #url(r'^$', views.home, name='home'),
    url(r'^jobdetail/(?P<pk>\d+)/$', views.JobDetail.as_view(), name='job_detail'),
    url(r'^(?P<c4cjob_id>\d+)/acceptjob$', views.acceptJob, name='accept_job'),
    url(r'^(?P<c4cjob_id>\d+)/donejob$', views.doneJob, name='done_job'),
    url(r'^(?P<c4cjob_id>\d+)/confirmjob$', views.confirmJob, name='confirm_job'),
    url(r'^(?P<c4cjob_id>\d+)/reportjob$', views.reportJob, name='report_job'),
    url(r'^(?P<c4cjob_id>\d+)/canceljob$', views.cancelJob, name='cancel_job'),
    url(r'^(?P<c4cjob_id>\d+)/deletejob$', views.deleteJob, name='delete_job'),
    url(r'^userjobs/$', views.UserJobs.as_view(), name='user_jobs'),
    url(r'^createjob/$', views.createJob, name='create_job'),
    url(r'jobcreation/$',views.JobCreation, name='job_creation'),
)