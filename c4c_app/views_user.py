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

class UpdateForm(forms.Form):
    username = forms.CharField(label='Your name', max_length=100)
    password = forms.CharField(label='Password', max_length=10,widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=50)
    first_name = forms.CharField(label='First name', max_length=40)
    last_name = forms.CharField(label='Last name', max_length=40)
    address = forms.CharField(max_length=300)
    birthday = DateField(widget=widgets.AdminDateWidget)

def user_edit(request):
    template_name = 'c4cuser_edit.html'

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        user = get_object_or_404(User, pk=request.user.pk)
        c4cuser = get_object_or_404(C4CUser, pk=request.user)
        data = {'username':user.username, 'password':user.password, 'email': user.email, 'first_name':user.first_name, 'last_name': user.last_name, 'address': c4cuser.address, 'birthday': c4cuser.birthday}
        form = UpdateForm(request.POST,initial=data)

        # check whether it's valid:
        if form.is_valid():

            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])
            user.password = password
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            c4cuser.address = form.cleaned_data['address']
            c4cuser.birthday = form.cleaned_data['birthday']
            c4cuser.save()

            return HttpResponseRedirect('/')

    else:
        form = UpdateForm()

    return render(request, template_name, {'form': form.as_p()})

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
