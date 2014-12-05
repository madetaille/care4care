from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from c4c_app import views
urlpatterns = patterns('',

                       # Home
                       url(r'^$', views.Feeds.as_view(template_name='index.html'), name='home'),
                       # Jobs
                       url(r'^feeds/$', views.Feeds.as_view(), name='feeds'),
                       url(r'^jobdetail/(?P<pk>\d+)/$', views.JobDetail.as_view(), name='job_detail'),
                       url(r'^(?P<c4cjob_id>\d+)/acceptjob$', views.acceptJob, name='accept_job'),
                       url(r'^(?P<c4cjob_id>\d+)/donejob$', views.doneJob, name='done_job'),
                       url(r'^(?P<c4cjob_id>\d+)/confirmjob$', views.confirmJob, name='confirm_job'),
                       url(r'^(?P<c4cjob_id>\d+)/reportjob$', views.reportJob, name='report_job'),
                       url(r'^(?P<c4cjob_id>\d+)/canceljob$', views.cancelJob, name='cancel_job'),
                       url(r'^(?P<c4cjob_id>\d+)/deletejob$', views.deleteJob, name='delete_job'),
                       url(r'^userjobs/$', login_required(views.userJobs), name='user_jobs'),
                       url(r'^(?P<member_pk>\d+)/userjobs/$', views.userJobs, name='user_jobs'),
                       url(r'^userjobs/$', views.userJobs, name='user_jobs'),
                       url(r'^jobcreation/$', login_required(views.JobCreation.as_view()), name='job_creation'),
                       url(r'^(?P<pk>\d+)/jobupdate/$', login_required(views.JobUpdate.as_view()), name='job_update'),
                       # Gift
                       url(r'^donation/$', views.DonationCreation.as_view(), name='donation_creation'),
                       url(r'^donation_detail/(?P<pk>\d+)/$', views.DonationDetail.as_view(), name='donation_detail'),
                       url(r'^alldonationMade/$', views.AllDonation_made.as_view(), name='donation_list_M'),
                       url(r'^alldonationReceived/$', views.AllDonation_received.as_view(), name='donation_list_R'),
                       url(r'^error/$', login_required(views.DonationError), name='donation_error'),
                       # User
                       url(r'^userdetail/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user_detail'),
                       url(r'^useredit/(?P<pk>\d+)/$', views.UserEdit.as_view(), name='user_edit'),
                       url(r'^c4cedit/(?P<pk>\d+)/$', views.C4CUserEdit.as_view(), name='c4cuser_edit'),
                       url(r'^chpassword/(?P<pk>\d+)/$', views.chPassword, name='chPassword'),
                       url(r'^network/$', views.PersonalNetwork.as_view(), name='network'),
                       url(r'^(?P<c4cuser_pk>\d+)/addnetwork', views.addNetwork, name='add_network'),
                       url(r'^registration/$', views.view_registration, name='registration'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       #Reset password
                        url(r'^resetpass/$', views.resetpassword, name='resetpass'),
                       # history
                       url(r'^history/$', views.History.as_view(), name='history'),
                       # News
                       url(r'^News/$', views.NewsCreation.as_view(), name='news_creation'),
                       url(r'^news_detail/(?P<pk>\d+)/$', views.NewsDetail.as_view(), name='news_detail'),
                       url(r'^allNewsBranch/$', views.AllNewsBranch.as_view(), name='all_news_list_Branch'),
                       url(r'^allNews/$', views.AllNews.as_view(), name='all_news_list'),
                       # Branch
                       url(r'^branchdetail/(?P<pk>\w+)/$', views.BranchDetail.as_view(), name='branch_detail'),
                       url(r'^addtobranch/(?P<pk>\w+)/$', views.add_to_branch, name='add_to_branch'),
                       url(r'^removefrombranch/(?P<pk>\w+)/$', views.remove_from_branch, name='remove_from_branch'),
                       url(r'^branchlist/$',views.BranchList.as_view(), name='branchlist'),
                       # Agenda
                       url(r'^agenda/$', login_required(views.AgendaYear), name='agenda'),
                       url(r'^agenda/(\d+)/$', login_required(views.AgendaYear), name='agenda'),
                       url(r'^agenda/(\d+)/(\d+)/$', login_required(views.AgendaYear), name='agenda'),
                       url(r'^month/(\d+)/(\d+)/(\d+)/$', login_required(views.AgendaMonth), name='month'),
                       url(r'^month/(\d+)/(\d+)/(\d+)/(prev|next)/$', login_required(views.AgendaMonth), name='month'),
                       url(r'^day/(\d+)/(\d+)/(\d+)/(\d+)/$', login_required(views.AgendaDay), name='day'),
                       url(r'^editevent/$', login_required(views.AgendaEditEvent), name='editevent'),
                       url(r'^editevent/(\d+)/$', login_required(views.AgendaEditEvent), name='editevent'),
                       url(r'^event/(\d+)/$', login_required(views.AgendaEvent), name='event'),
                       # Stat
                       url(r'^stat/$', views.stat, name='stat'),
                       # News
                       #url(r'^news/$', views.news, name = 'news'),
                       # What is Care 4 Care ?
                       url(r'^whatisc4c/$', views.whatisc4c, name='whatisc4c'),
                       url(r'^aboutus/$', views.aboutus, name='aboutus'),
                       url(r'^sendemail/(?P<pk>\d+)/$', login_required(views.send_email),name = 'send_email'),
                       url(r'^sendemailuser/(?P<pk>\d+)/$', login_required(views.send_email_user),name = 'send_user_email')
                       )
