from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from c4c_app.models import C4CDonation
from c4c_app.models import C4CUser
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
#from c4c_app.forms import ContactForm

class DonationCreation(CreateView):

    fields = [ 'receiver', 'date', 'message', 'amount']
    model = C4CDonation
    template_name = 'donation_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.donation_bool = False
        sender = get_object_or_404(C4CUser, user=self.request.user)
        success_url = '/donation_detail/'
        amount = int(self.request.POST['amount'])

        if(sender.time_account > amount ):
            self.object.sender = sender.user
            self.object.receiver = get_object_or_404(C4CUser, pk=self.request.POST['receiver']).user
            self.object.date = self.request.POST['date']
            self.object.message = self.request.POST['message']
            self.object.amount = self.request.POST['amount']
            self.object.save()
            self.donation_bool = True
        else:
            self.donation_bool = False

        self.object.save()
        return HttpResponseRedirect(reverse("c4c:donation_detail", args=(self.object.id,)))

    def __str__(self):
        return self.name

class DonationDetail(generic.DetailView):
    model = C4CDonation
    template_name = 'donation_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DonationDetail, self).get_context_data(**kwargs)
        # Add in the publisher
        member = get_object_or_404(C4CUser, user=self.request.user)
        context['member'] = member
        return context

class AllDonation(generic.ListView):
    template_name = 'c4cdonation_list.html'
    context_object_name = 'allDonationList'
    model = C4CDonation

    def get_queryset(self):
        user = get_object_or_404(C4CUser, user = self.request.user)
        donations = C4CDonation.objects.filter(sender = self.request.user)

        return donations



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