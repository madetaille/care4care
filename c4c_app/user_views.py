from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from c4c_app.models import *

class PersonalNetwork(generic.ListView):
    template_name = 'network.html'
    context_object_name = 'network_list'
    
    def get_queryset(self):
        member = get_object_or_404(C4CUser, user=self.request.user)
        res=[]
        res.append(member.jobs_created.all())
        res.append(member.jobs_asked.all())
        res.append(member.jobs_accepted.all())
        return res 