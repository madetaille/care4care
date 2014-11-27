from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from c4c_app.models import C4CDonation
from c4c_app.models import C4CUser

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
    return  #redirect("/donation_form.html")



def donation_as_views():

    return  #redirect("/donation_form.html")
