from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms.fields import DateField
from django.contrib.admin import widgets
from django import forms
from django.contrib.auth.hashers import make_password

from c4c_app.models import C4CUser

class UserDetail(generic.DetailView):
    model = C4CUser
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserDetail, self).get_context_data(**kwargs)
        viewer = get_object_or_404(C4CUser, user=self.request.user)
        context['viewer'] = viewer
        return context

class UserEdit(generic.edit.UpdateView):
    template_name = 'base_user_edit.html'
    model = User
    fields = ['username','first_name','last_name','email']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(self.object.pk,)))

class C4CUserEdit(generic.edit.UpdateView):
    template_name = 'c4cuser_edit.html'
    model = C4CUser
    fields = ['address','birthday']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(self.object.pk,)))

class PersonalNetwork(generic.ListView):
    template_name = 'network.html'
    context_object_name = 'network_list'

    def get_queryset(self):
        member = get_object_or_404(C4CUser, user=self.request.user)
        return member.network.all()

def addNetwork(request, c4cuser_pk):
    user_to_add = get_object_or_404(C4CUser,pk = c4cuser_pk)
    user = get_object_or_404(C4CUser,pk = request.user)

    user.network.add(user_to_add)
    return HttpResponseRedirect(reverse('c4c:network'))
