from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from c4c_app.models import C4CUser, C4CJob


class JobCreation(CreateView):
    model = C4CJob
    template_name = 'c4cjob_form.html'

    fields = ['title', 'description', 'location', 'start_date']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        maker = get_object_or_404(C4CUser, user=self.request.user)
        self.object.created_by = maker

        typ = self.request.POST['kind']
        if typ == 'offer':
            self.object.offer = True
        else:
            self.object.offer = False

        if(form.instance.offer):
            self.object.done_by = maker
        else:
            self.object.asked_by = maker

        self.object.save()
        return HttpResponseRedirect(reverse('c4c:job_detail', args=(self.object.id,)))

class JobUpdate(UpdateView):
    model = C4CJob
    template_name = 'c4cjob_update_form.html'
        
    fields = ['title', 'description', 'location', 'start_date']

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.save()
        return HttpResponseRedirect(reverse('c4c:job_detail', args=(self.object.id,)))
    
    
class JobDetail(generic.DetailView):
    model = C4CJob
    template_name = 'job_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(JobDetail, self).get_context_data(**kwargs)
        # Add in the publisher
        member = get_object_or_404(C4CUser, user=self.request.user)
        context['member'] = member
        return context


def acceptJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)
    user_site = get_object_or_404(C4CUser, user=request.user)

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
    job = get_object_or_404(C4CJob, pk=c4cjob_id)
    job.duration = request.POST['duration']
    job.end_date = timezone.now()
    job.save()
    # TODO: avertir le createur de la completion du job
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


def confirmJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)
    job.complete = True
    job.save()
    # TODO: avertir le createur de la completion du job
    # TODO: avertir le travailleur de la completion du job
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


def reportJob(request, c4cjob_id):
    # TODO: envoie d un email a l admin
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(c4cjob_id,)))


def cancelJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)

    # TODO: avertir demandeur/offreur par email
    if job.offer == False:
        job.done_by = None
    else:
        job.asked_by = None
    job.save()

    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


def deleteJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)

    # TODO: envoie email pour avertir autre personne qui a accepte
    job.delete()
    return HttpResponseRedirect(reverse('c4c:user_jobs'))


class UserJobs(generic.ListView):
    template_name = 'user_job.html'
    context_object_name = 'user_job_list'

    def get_queryset(self):
        member = get_object_or_404(C4CUser, user=self.request.user)
        res = []
        res.append(member.jobs_created.all())
        res.append(member.jobs_asked.all())
        res.append(member.jobs_accepted.all())
        return res
