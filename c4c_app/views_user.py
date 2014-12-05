from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms.fields import DateField, EmailField
from django.contrib.admin import widgets
from django import forms
from django.contrib.auth import authenticate, login

from django.utils.translation import ugettext as _

from c4c_app.models import C4CUser
from c4c_app.views_error403 import error403
from c4c import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template import Context

class UserDetail(generic.DetailView):
    model = C4CUser
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserDetail, self).get_context_data(**kwargs)
        viewer = get_object_or_404(C4CUser, user=self.request.user)
        context['viewer'] = viewer

        # get branches
        context['branches'] = self.object.get_branches()
        context['not_empty_br'] = len(self.object.get_branches()) != 0
        return context

class UserEdit(generic.edit.UpdateView):
    template_name = 'base_user_edit.html'
    model = User
    fields = ['username','first_name','last_name','email']

    def post(self, request, **kwargs):
        ret = super(UserEdit, self).post(request, **kwargs)
        ownerpk = int(self.kwargs.get('pk'))
        viewer = get_object_or_404(User, pk=self.request.user.pk)
        viewerpk = viewer.pk

        if viewerpk != ownerpk:
            return error403(self.request)
        else:
            return ret

    def get(self, request, **kwargs):
        ret = super(UserEdit, self).get(request, **kwargs)
        ownerpk = int(self.kwargs.get('pk'))
        viewer = get_object_or_404(User, pk=self.request.user.pk)
        viewerpk = viewer.pk

        if viewerpk != ownerpk:
            return error403(self.request)
        else:
            return ret

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(self.object.pk,)))

class C4CUserEdit(generic.edit.UpdateView):
    template_name = 'c4cuser_edit.html'
    model = C4CUser
    fields = ['address','birthday']

    def post(self, request, **kwargs):
        ret = super(C4CUserEdit, self).post(request, **kwargs)
        ownerpk = int(self.kwargs.get('pk'))
        viewer = get_object_or_404(User, pk=self.request.user.pk)
        viewerpk = viewer.pk

        if viewerpk != ownerpk:
            return error403(self.request)
        else:
            return ret

    def get(self, request, **kwargs):
        ret = super(C4CUserEdit, self).get(request, **kwargs)
        ownerpk = int(self.kwargs.get('pk'))
        viewer = get_object_or_404(User, pk=self.request.user.pk)
        viewerpk = viewer.pk

        if viewerpk != ownerpk:
            return error403(self.request)
        else:
            return ret

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(self.object.pk,)))

class PasswordForm(forms.Form):
    pass1 = forms.CharField(label=_('Password'), max_length=10,widget=forms.PasswordInput)
    pass2 = forms.CharField(label=_('Confirm Password'), max_length=10,widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(PasswordForm,self).clean()
        password = cleaned_data.get('pass1')
        cpassword = cleaned_data.get('pass2')

        if password != cpassword:
            raise forms.ValidationError(_('The two typed passwords are different.'))

def chPassword(request,pk):
    template_name = 'change_password.html'

    # check access permission
    if int(pk) != request.user.pk:
        return error403(request)

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():

            username = str(request.user.username)
            formpass = form.cleaned_data['pass1']
            request.user.set_password(formpass)
            request.user.save()

            user = authenticate(username=username,password=formpass)
            login(request,user)
            return HttpResponseRedirect(reverse('c4c:user_detail', args=(user.pk,)))
    else:
        form = PasswordForm()

    return render(request, template_name, {'form': form.as_p()})

class ResetPassForm(forms.Form):
    email = EmailField(label=_('Email'), max_length=50)

    def clean(self):
        cleaned_data = super(ResetPassForm,self).clean()
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

            d = Context({'password' : password, 'user_email' : user})
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    
            return HttpResponseRedirect(reverse('c4c:login'))

    else:
        form = ResetPassForm()

    return render(request, template_name, {'form': form})

