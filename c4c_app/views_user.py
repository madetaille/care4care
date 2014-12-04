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
from django.contrib.auth import authenticate, login

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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserEdit, self).get_context_data(**kwargs)
        viewer = get_object_or_404(User, pk=self.request.user.pk)
        context['viewerpk'] = viewer.pk
        context['ownerpk'] = int(self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(self.object.pk,)))

class C4CUserEdit(generic.edit.UpdateView):
    template_name = 'c4cuser_edit.html'
    model = C4CUser
    fields = ['address','birthday']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(C4CUserEdit, self).get_context_data(**kwargs)
        viewer = get_object_or_404(C4CUser, user=self.request.user)
        context['viewerpk'] = viewer.user.pk
        context['ownerpk'] = int(self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(self.object.pk,)))

class PasswordForm(forms.Form):
    pass1 = forms.CharField(label='Password', max_length=10,widget=forms.PasswordInput)
    pass2 = forms.CharField(label='Confirm Password', max_length=10,widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(PasswordForm,self).clean()
        password = cleaned_data.get('pass1')
        cpassword = cleaned_data.get('pass2')

        if password != cpassword:
            raise forms.ValidationError('The two typed passwords are different.')

def chPassword(request,pk):
    template_name = 'change_password.html'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            username = str(request.user.username)
            formpass = form.cleaned_data['pass1']
            request.user.set_password(formpass)
            request.user.save()

            user = authenticate(username=username,password=formpass)
            login(request,user)
            return HttpResponseRedirect(reverse('c4c:user_detail', args=(user.pk,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordForm()

    return render(request, template_name, {'form': form.as_p(), 'ownerpk': int(pk), 'viewerpk': request.user.pk})

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
