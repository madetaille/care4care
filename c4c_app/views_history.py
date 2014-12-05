from c4c_app.models import C4CDonation, C4CUser, C4CJob
from django.views import generic

class History(generic.ListView):
    """ For the history of a user """
    
    model = C4CUser
    template_name = 'history.html'
    context_object_name = 'history'

    def get_queryset(self):
        history_list = []

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
