from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from c4c_app.models import *

def createJob(request, c4cuser_id):
    maker = get_object_or_404(C4CUser, pk = c4cuser_id)
    try:
        user = C4CUser.objects.get(pk=request.POST['user'])    
    except (KeyError, C4CUser.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'create_job.html', {
            'error_message': "You enter an invalide user.",
        })
    else:
        job = None
        if(request.POST['kind'] == 'offer'):
            job = C4CJob(created_by = maker, done_by = user, title = request.POST['title'],
                         description = request.POST['description'], location = request.POST['location'],
                         duration = request.POST['duration'], start_date = request.POST['start'],
                         end_date = request.POST['end'], complete = False)
        else:
            job = C4CJob(created_by = maker, asked_by = user, title = request.POST['title'],
                         description = request.POST['description'], location = request.POST['location'],
                         duration = request.POST['duration'], start_date = request.POST['start'],
                         end_date = request.POST['end'], complete = False)
        job.save()
        
        return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))

class JobDetail(generic.DetailView):
    model = C4CJob
    template_name = 'job_detail.html'
    
class UserJobs(generic.ListView):
    template_name = 'user_job.html'
    context_object_name = 'user_job_list'
    
    def get_queryset(self):
        self.user = get_object_or_404(C4CUser, c4cuser_id = self.args[0])
        return C4CJob.objects.filter(created_by = self.user)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserJobs, self).get_context_data(**kwargs)
        # Add in the publisher
        context['user'] = self.user
        return context