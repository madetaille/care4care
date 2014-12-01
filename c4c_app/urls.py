from django.conf.urls import patterns, url

from c4c_app import views

urlpatterns = patterns('',
    #Home
    url(r'^$', views.home, name='home'),
    #Jobs
    url(r'^jobdetail/(?P<pk>\d+)/$', views.JobDetail.as_view(), name='job_detail'),
    url(r'^(?P<c4cjob_id>\d+)/acceptjob$', views.acceptJob, name='accept_job'),
    url(r'^(?P<c4cjob_id>\d+)/donejob$', views.doneJob, name='done_job'),
    url(r'^(?P<c4cjob_id>\d+)/confirmjob$', views.confirmJob, name='confirm_job'),
    url(r'^(?P<c4cjob_id>\d+)/reportjob$', views.reportJob, name='report_job'),
    url(r'^(?P<c4cjob_id>\d+)/canceljob$', views.cancelJob, name='cancel_job'),
    url(r'^(?P<c4cjob_id>\d+)/deletejob$', views.deleteJob, name='delete_job'),
    url(r'^userjobs/$', views.userJobs, name='user_jobs'),
    url(r'^(?P<member_pk>\d+)/userjobs/$', views.userJobs, name='user_jobs'),
    url(r'^jobcreation/$',views.JobCreation.as_view(), name='job_creation'),
    url(r'^(?P<pk>\d+)/jobupdate/$',views.JobUpdate.as_view(), name='job_update'),
    url(r'^alljobs/$',views.AllJobs.as_view(), name='all_jobs'),
    url(r'^donation/$', views.DonationCreation.as_view(), name='donation_creation'),
    url(r'^donation_detail/(?P<pk>\d+)/$', views.DonationDetail.as_view(), name='donation_detail'),
    url(r'^alldonation/$', views.AllDonation.as_view(), name='c4cdonation_list'),
    #User
    url(r'^userdetail/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user_detail'),
    url(r'^useredit/$', views.user_edit, name='user_edit'),
    url(r'^network/$', views.PersonalNetwork.as_view(), name='network'),
    url(r'^(?P<c4cuser_pk>\d+)/addnetwork', views.addNetwork, name='add_network'),
    url(r'^registration/$', views.view_registration, name='registration'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^donation/(?P<receiver_id>\d+)/(?P<amount>\d+)/(?P<date>\d+)/(?P<message>\d+)/$', views.donation, name='donation'),
    #Branch
    url(r'^branchdetail/(?P<pk>\d+)/$', views.BranchDetail.as_view(), name='branch_detail'),
    #Agenda
    url(r'^agenda/$', views.year, name='agenda'),
    url(r'^agenda/(\d+)/$', views.year, name='agenda'),
    url(r'^agenda/(\d+)/(\d+)/$', views.year, name='agenda'),
    url(r'^month/(\d+)/(\d+)/(\d+)/$', views.month, name='month'),
    url(r'^month/(\d+)/(\d+)/(\d+)/(prev|next)/$', views.month, name='month'),
    url(r'^day/(\d+)/(\d+)/(\d+)/(\d+)/$', views.day, name='day'),

)
