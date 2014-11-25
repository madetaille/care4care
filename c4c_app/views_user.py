from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from c4c_app.models import *

class UserDetail(generic.DetailView):
    model = C4CUser
    template_name = 'user_detail.html'

class PersonalNetwork(generic.ListView):
    template_name = 'network.html'
    context_object_name = 'network_list'
    
    def get_queryset(self):
        member = get_object_or_404(C4CUser, user=self.request.user)
        return member.network.all()