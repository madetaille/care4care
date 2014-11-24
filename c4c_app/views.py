from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from c4c_app.models import *

# class JobCreation(generic.):

class JobDetail(generic.DetailView):
    model = C4CJob
    template_name = 'job_detail.html'
    
class UserJobs(generic.ListView):
    template_name = 'user_job.html'
    context_object_name = 'user_job_list'
    
    def get_queryset(self):
        self.user = get_object_or_404(C4CUser, C4CUser_id = self.args[0])
        return C4CJob.objects.filter(created_by = self.user)