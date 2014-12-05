from django.contrib.auth.models import User
from c4c_app.models import C4CUser
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms.fields import DateField
from django.contrib.admin import widgets

from django.utils import translation
from django.utils.translation import ugettext as _

class UserForm(forms.Form):
    username = forms.CharField(label=_('Your name'), max_length=100)
    password = forms.CharField(label=_('Password'), max_length=10,widget=forms.PasswordInput)
    email = forms.EmailField(label=_('Email'), max_length=50)
    first_name = forms.CharField(label=_('First name'), max_length=40)
    last_name = forms.CharField(label=_('Last name'), max_length=40)
    address = forms.CharField(max_length=300)
    birthday = DateField(widget=widgets.AdminDateWidget)


def view_registration(request):
    template_name = 'user_registration.html'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            c4cuser = C4CUser(user=user, address=form.cleaned_data['address'], birthday=form.cleaned_data['birthday'])
            c4cuser.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, template_name, {'form': form.as_p()})

"""def view_registration(request):
    template_name = 'user_registration.html'



"firstname=form.cleaned_data['first_name'], lastname=form.cleaned_data['last_name'])



    username = request.Post('username')
    password = request.Post('password')
    email = request.Post('email')
    firstname = request.Post('first name')
    lastname = request.Post('last name')
    address = request.Post('address')
    birthday = request.Post('birthday')

    user = User.objects.create_user(username, email, password, firstname=firstname, lastname=lastname)

    user.C4CUser.address = address
    user.C4CUser.birthday = birthday
    user.save()"""
