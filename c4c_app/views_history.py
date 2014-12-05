from django.shortcuts import get_object_or_404
from c4c_app.models import C4CDonation, C4CUser, C4CNews, C4CJob
from django.views import generic

class History(generic.ListView):

    model = C4CUser
    template_name = 'history.html'
    context_object_name = 'history'

    def get_queryset(self):
        history_list = []
        #donations_sent = []
        #donation_received = []
        #job_demanded = []
        #job_forbidden = []


        user = get_object_or_404(C4CUser, user = self.request.user)

        #donation made by the user
        donations_sent = C4CDonation.objects.filter(sender = self.request.user)
        history_list.append(donations_sent)

        #donation received by the user
        donations_received = C4CDonation.objects.filter(receiver = self.request.user)
        history_list.append(donations_received)

        #Job asked by the user
        job_demanded = C4CJob.objects.filter(asked_by = self.request.user)
        history_list.append(job_demanded)

        #job done by the user
        job_done = C4CJob.objects.filter(done_by = self.request.user)
        history_list.append(job_done)

        return history_list
