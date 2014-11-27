from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from c4c_app.models import C4CDonation
from c4c_app.models import C4CUser
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

class DonationCreation(CreateView):

    fields = ['sender', 'receiver', 'date', 'message', 'amount']
    model = C4CDonation
    template_name = 'donation_form.html'

    #def donation_as_views():
    #   return HttpResponseRedirect(reverse('c4c:job_detail', args=(1,)))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        sender = get_object_or_404(C4CUser, user=self.request.user)

        if(sender.time_account > self.request.POST['amount']):
            self.object.sender = sender
            self.object.receiver = get_object_or_404(C4CUser, pk=self.request.POST['receiver'])
            self.objct.date = self.request.POST['date']
            self.objct.message = self.request.POST['message']
            self.object.amount = self.request.POST['amount']
            self.object.save()
            donation_bool = True
        else:
            donation_bool = True

        return HttpResponseRedirect(reverse('c4c:donation_detail', args=(self.object.id,donation_bool,)))


def donation(sender_id, receiver_id, amount, date, message):
    #create Donation
    don = C4CDonation(sender_id, receiver_id, amount, date, message)


 #compute time from user
    sender = get_object_or_404(C4CUser, pk=sender_id.user.id)
    receiver = get_object_or_404(C4CUser, pk=receiver_id)
    sender.time_account -= amount
    sender.save()
    receiver.time_account += amount
    receiver.save()

    don.save()
    #return  HttpResponseRedirect("/")