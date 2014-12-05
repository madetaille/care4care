import datetime
from smtplib import *

from django import forms
from django.contrib.admin import widgets
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.forms.fields import DateField, EmailField, ImageField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views import generic

from c4c import settings
from c4c_app.models import C4CUser, C4CBranch
from c4c_app.views_error403 import error403
class UserDetail(generic.DetailView):
    model = C4CUser
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserDetail, self).get_context_data(**kwargs)
        viewer = get_object_or_404(C4CUser, user=self.request.user)
        context['viewer'] = viewer

        context['is_in_network'] = viewer == context['c4cuser'] or context['c4cuser'].network.filter(pk=viewer.user.pk).exists()
        context['is_in_my_network'] = viewer == context['c4cuser'] or viewer.network.filter(pk=context['c4cuser'].user.pk).exists()

        # get branches
        context['branches'] = self.object.get_branches()
        return context


class UserForm(forms.Form):
    password = forms.CharField(label=_('Password'), max_length=10, widget=forms.PasswordInput, required=False)
    password_confirm = forms.CharField(label=_('Password (confirmation)'), max_length=10, widget=forms.PasswordInput, required=False)
    address = forms.CharField(max_length=300)
    birthday = DateField(widget=widgets.AdminDateWidget)
    avatar = ImageField(label=_('Avatar image'), required=False)
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
        return cleaned_data


def UserEdit(request):
    template_name = 'base_user_edit.html'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            request.user.c4cuser.address = form.cleaned_data['address']
            request.user.c4cuser.birthday = form.cleaned_data['birthday']
            if form.cleaned_data['avatar'] is not None and form.cleaned_data['avatar']:
                request.user.c4cuser.avatar = form.cleaned_data['avatar']
            for branch in C4CBranch.objects.all():
                branch.group.user_set.remove(request.user)
            for branch in form.cleaned_data['branches']:
                request.user.groups.add(C4CBranch.objects.get(pk=branch).group)
            request.user.c4cuser.save()
            if form.cleaned_data['password'] is not None and form.cleaned_data['password'] != "":
                request.user.set_password(form.cleaned_data['password'])

            return HttpResponseRedirect(reverse('c4c:user_detail', args=(request.user.pk,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        print([a.pk for a in request.user.c4cuser.get_branches()])
        form = UserForm(initial={"address": request.user.c4cuser.address, "birthday": request.user.c4cuser.birthday, "branches": [a.pk for a in request.user.c4cuser.get_branches()]})

    return render(request, template_name, {'form': form.as_p()})


class ResetPassForm(forms.Form):
    email = EmailField(label=_('Email'), max_length=50)

    def clean(self):
        cleaned_data = super(ResetPassForm, self).clean()
        mailaddr = cleaned_data.get('email')

        try:
            user = User.objects.get(email=mailaddr)
        except ObjectDoesNotExist:
            raise forms.ValidationError(_('There is no account with this email address.'))


def resetpassword(request):
    template_name = 'resetpassword.html'

    # check access permission
    if request.user.is_authenticated():
        return error403(request)

    if request.method == 'POST':
        form = ResetPassForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = User.objects.make_random_password()
            user = get_object_or_404(User, email=email)
            user.set_password(password)
            user.save()

            subject = _('Reset of your password !')
            from_email, to = settings.EMAIL_HOST_USER, email

            htmly = get_template('email_reset_password.html')

            d = Context({'password': password, 'user_email': user})
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except SMTPDataError:
                return HttpResponseRedirect(reverse('c4c:login'))

            return HttpResponseRedirect(reverse('c4c:login'))

    else:
        form = ResetPassForm()

    return render(request, template_name, {'form': form})
