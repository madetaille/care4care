from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from c4c_app.models import *

def createJob(request):
    maker = get_object_or_404(C4CUser, user=request.user)
    job = None
    if(request.POST['kind'] == 'offer'):
        job = C4CJob(created_by = maker, done_by = maker, title = request.POST['title'],
                     description = request.POST['description'], location = request.POST['location'],
                     duration = request.POST['duration'], start_date = request.POST['start'],
                     end_date = request.POST['end'])
    else:
        job = C4CJob(created_by = maker, done_by = maker, title = request.POST['title'],
                     description = request.POST['description'], location = request.POST['location'],
                     duration = request.POST['duration'], start_date = request.POST['start'],
                     end_date = request.POST['end'])
    job.save()
        
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))

class JobDetail(generic.DetailView):
    model = C4CJob
    template_name = 'job_detail.html'
    
def acceptJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk = c4cjob_id)
    user_job = job.created_by
    user_site = get_object_or_404(C4CUser, user = request.user)
    if user_site == user_job:
        return render(request, 'job_detail.html', {
            'c4cjob' : job,
            'error_message': "You can't accept a demand/offer that you created !.",
        })
    else:
        if job.done_by == None:
            job.done_by = user_site
            job.save()
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id)))
        else:
            job.asked_by = user_site
            job.save()
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id)))

def confirmJob(request, c4cjob_id):
    return
    
class UserJobs(generic.ListView):
    template_name = 'user_job.html'
    context_object_name = 'user_job_list'
    
    def get_queryset(self):
        self.membre = get_object_or_404(C4CUser, user=self.request.user)
        return self.membre.jobs_created  #C4CJob.objects.filter(created_by = self.membre)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserJobs, self).get_context_data(**kwargs)
        # Add in the publisher
        context['user'] = self.membre
        return context
    