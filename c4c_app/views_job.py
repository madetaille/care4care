from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
import datetime

from c4c import settings
from c4c_app.models import C4CUser, C4CJob, C4CEvent
class JobCreation(CreateView):
    model = C4CJob
    template_name = 'c4cjob_form.html'

    fields = ['title', 'description', 'location', 'start_date']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        maker = get_object_or_404(C4CUser, user=self.request.user)
        self.object.created_by = maker.user

        typ = self.request.POST['kind']
        if typ == 'offer':
            self.object.offer = True
        else:
            self.object.offer = False

        if(form.instance.offer):
            self.object.done_by = maker.user
        else:
            self.object.asked_by = maker.user

        self.object.save()

        """send an email"""
        job = get_object_or_404(C4CJob, id=self.object.id)
        send_email_creation_job(job, maker)

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

        member = None
        if self.request.user.is_authenticated():
            member = get_object_or_404(C4CUser, user=self.request.user)

        context['member'] = member
        return context


@login_required
def acceptJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)
    user_site = get_object_or_404(C4CUser, user=request.user)

    if job.offer == False:
        if user_site.user == job.asked_by:
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))
        else:
            job.done_by = user_site.user
            job.save()
            event1 = C4CEvent(name=job.title, date=job.start_date, job=job, user=job.asked_by, description=job.description)
            event2 = C4CEvent(name=job.title, date=job.start_date, job=job, user=job.done_by, description=job.description)
            event1.save()
            event2.save()
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))
    else:
        if user_site.user == job.done_by:
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))
        else:
            job.asked_by = user_site.user
            job.save()
            event1 = C4CEvent(name=job.title, date=job.start_date, job=job, user=job.asked_by, description=job.description)
            event2 = C4CEvent(name=job.title, date=job.start_date, job=job, user=job.done_by, description=job.description)
            event1.save()
            event2.save()
            return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


@login_required
def doneJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)
    job.duration = request.POST['Duration']
    job.end_date = timezone.now()
    job.save()
    event = get_object_or_404(C4CEvent, job=job, user=request.user)
    event.delete()

    send_email_done_job(job)
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


@login_required
def confirmJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)
    job.complete = True
    job.save()

    event = get_object_or_404(C4CEvent, job=job, user=request.user)
    event.delete()
    send_email_confirm(job)
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


@login_required
def reportJob(request, c4cjob_id):
    # TODO: envoie d un email a l admin
    return HttpResponseRedirect(reverse('c4c:job_detail', args=(c4cjob_id,)))


@login_required
def cancelJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)

    # TODO: avertir demandeur/offreur par email
    if job.offer == False:
        event1 = get_object_or_404(C4CEvent, job=job, user=job.done_by.user)
        event2 = get_object_or_404(C4CEvent, job=job, user=job.asked_by.user)
        event1.delete()
        event2.delete()
        job.done_by = None
    else:
        event1 = get_object_or_404(C4CEvent, job=job, user=job.done_by.user)
        event2 = get_object_or_404(C4CEvent, job=job, user=job.asked_by.user)
        event1.delete()
        event2.delete()
        job.asked_by = None
    job.save()

    return HttpResponseRedirect(reverse('c4c:job_detail', args=(job.id,)))


@login_required
def deleteJob(request, c4cjob_id):
    job = get_object_or_404(C4CJob, pk=c4cjob_id)

    if(job.asked_by is not None and job.done_by is not None):
        event1 = get_object_or_404(C4CEvent, job=job, user=job.done_by.user)
        event2 = get_object_or_404(C4CEvent, job=job, user=job.asked_by.user)
        event1.delete()
        event2.delete()
    # TODO: envoie email pour avertir autre personne qui a accepte
    job.delete()
    return HttpResponseRedirect(reverse('c4c:user_jobs'))


@login_required
def userJobs(request, member_pk=None):

    member = None
    if member_pk:
        member = get_object_or_404(C4CUser, pk=member_pk)
    else:
        member = get_object_or_404(C4CUser, user=request.user)

    res = []
    res.append(member.user.jobs_asked.filter(complete=False).order_by("-start_date"))
    res.append(member.user.jobs_accepted.filter(complete=False).order_by("-start_date"))
    res.append(member.user.jobs_created.all().order_by("-start_date"))
    res.append(member.user.jobs_asked.all().order_by("-start_date"))
    res.append(member.user.jobs_accepted.all().order_by("-start_date"))

    context = {'user_job_list': res}

    return render(request, 'user_job.html', context)


class Feeds(generic.ListView):
    template_name = 'all_jobs.html'
    context_object_name = 'all_jobs_list'

    def get_queryset(self):
        users = None
        if self.request.user.is_authenticated():
            user = get_object_or_404(C4CUser, user=self.request.user)
            users = set()
            for branch in user.get_branches():
                users = set(branch.get_users()).union(users)
            users = [u.c4cuser for u in users]
        else:
            users = C4CUser.objects.all()

        jobs = []
        res = []
        for usr in users:
            jobs.append(C4CJob.objects.filter(created_by=usr.user, complete=False, start_date__gte=datetime.date.today()))

        demands = []
        offers = []
        for jobs_usr in jobs:
            for job in jobs_usr:
                if(job.offer):
                    offers.append(job)
                else:
                    demands.append(job)
        
        demands.sort(key=lambda x: x.start_date, reverse=True)
        offers.sort(key=lambda x: x.start_date, reverse=True)
        res.append(demands)
        res.append(offers)
        return res


def send_email_creation_job(job, maker):
        subject, from_email, to = 'Care4Care : you created a job !', settings.EMAIL_HOST_USER, maker.user.email
        text_content = ''
        htmly = get_template('email_jobcreation.html')
        
        d = Context({ 'c4cjob': job })
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()



def send_email_done_job(job):
    subject, from_email, to = 'Care4Care : a job is waiting for you to be completed !', settings.EMAIL_HOST_USER, job.asked_by.email
    
    
    htmly = get_template('email_jobcompleted.html')
    text_content = ''

    d = Context({'c4cjob': job})
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def send_email_confirm(job):
    subject, from_email, to = 'Care4Care : a job you did has been confirmed !', settings.EMAIL_HOST_USER, job.done_by.email
    
    htmly = get_template('email_jobconfirmed.html')
    text_content = ''

    d = Context({'c4cjob': job})
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    
