from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from c4c_app.models import *

def createJob(request):
    maker = get_object_or_404(C4CUser, user=request.user)
    job = None
    if(request.POST['kind'] == 'offer'):
        job = C4CJob(created_by = maker, done_by = maker, 
                     title = request.POST['title'],
                     description = request.POST['description'], 
                     location = request.POST['location'], 
                     start_date = request.POST['start'])
    else:
        job = C4CJob(created_by = maker, done_by = maker, 
                     title = request.POST['title'],
                     description = request.POST['description'], 
                     location = request.POST['location'],
                     start_date = request.POST['start'])
    job.save()
        
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))

class JobCreation(generic.DetailView):
    model = C4CJob
    template_name = 'create_job.html'
    
    

class JobDetail(generic.DetailView):
    model = C4CJob
    template_name = 'job_detail.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(JobDetail, self).get_context_data(**kwargs)
        # Add in the publisher
        context['member'] = get_object_or_404(C4CUser, user=self.request.user)
        return context
    
    
def acceptJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk = c4cjob_id)
    user_site = get_object_or_404(C4CUser, user = request.user)

    if job.offer == False:
        if user_site == job.asked_by:
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))
        else:
            job.done_by = user_site
            job.save()
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))
    else:
        if user_site == job.done_by:
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))
        else:
            job.asked_by = user_site
            job.save()
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))

def doneJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk = c4cjob_id)
    job.duration = request.POST['duration']
    job.end_date = timezone.now()
    job.save()
    # avertir le createur de la completion du job
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))
    
    
def confirmJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk = c4cjob_id)
    job.complete = True
    job.save()
    # avertir le createur de la completion du job 
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))

def reportJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk = c4cjob_id)
    # envoie d un email a l admin
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


def cancelJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk = c4cjob_id)
    
    # avertir demandeur/offreur par email
    if job.offer == False:
        job.done_by = None
    else:
        job.asked_by = None
    job.save()
    
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


def deleteJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk = c4cjob_id)
    
    #envoie email pour avertir autre personne qui a accepte
    job.delete()
    return HttpResponseRedirect(reverse('c4c:user_jobs'))


class UserJobs(generic.ListView):
    template_name = 'user_job.html'
    context_object_name = 'user_job_list'
    
    def get_queryset(self):
        member = get_object_or_404(C4CUser, user=self.request.user)
        res=[]
        res.append(member.jobs_created.all())
        res.append(member.jobs_asked.all())
        res.append(member.jobs_accepted.all())
        return res #C4CJob.objects.filter(created_by = self.membre)
    
