import datetime

from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.forms.fields import DateField, ImageField
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _

from c4c import settings
from c4c_app.models import C4CUser, C4CBranch

from smtplib import *

class UserForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=100)
    password = forms.CharField(label=_('Password'), max_length=10, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=_('Password (confirmation)'), max_length=10, widget=forms.PasswordInput)
    email = forms.EmailField(label=_('Email'), max_length=50)
    first_name = forms.CharField(label=_('First name'), max_length=40)
    last_name = forms.CharField(label=_('Last name'), max_length=40)
    address = forms.CharField(max_length=300)
    birthday = DateField(widget=widgets.AdminDateWidget)
    avatar = ImageField(label=_('Avatar image'))
    branches = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kw):
        super(UserForm, self).__init__(*args, **kw)
        self.fields['branches'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[(a.pk, a.name) for a in C4CBranch.objects.all()])

    def clean(self):
        """ Verify birthday and password"""
        cleaned_data = super(UserForm, self).clean()
        if "birthday" in cleaned_data and cleaned_data["birthday"] > datetime.date(datetime.date.today().year - 16, datetime.date.today().month, datetime.date.today().day):
            raise forms.ValidationError(_("You must be older than 16 years old!"))

        if "password" in cleaned_data and "password_confirm" in cleaned_data and cleaned_data["password"] != cleaned_data["password_confirm"]:
            raise forms.ValidationError(_("Passwords do not match"))
        if User.objects.filter(username = cleaned_data["username"]):
            raise forms.ValidationError(_("Username already exists"))
        #if get_object_or_404(C4CUser, user.username=cleaned_data["username"])
         #   raise forms.ValidationError(_("Username already exists"))
        return cleaned_data


def view_registration(request):
    template_name = 'user_registration.html'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():

            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            for branch in form.cleaned_data['branches']:
                user.groups.add(C4CBranch.objects.get(pk=branch).group)
            user.save()
            c4cuser = C4CUser(user=user, address=form.cleaned_data['address'], birthday=form.cleaned_data['birthday'])
            c4cuser.avatar = form.cleaned_data['avatar']
            c4cuser.save()

            subject = _('Your account has been successfully created !')
            from_email, to = settings.EMAIL_HOST_USER, user.email

            htmly = get_template('email_inscription.html')

            d = Context({'user': user, 'c4cuser': c4cuser})
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except SMTPDataError:
                return HttpResponseRedirect('/')

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, template_name, {'form': form.as_p()})
