from smtplib import *

from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.views import generic

from c4c import settings
from c4c_app.models import C4CUser

def send_email(request, pk):
    return render(request, "send_email.html", {'pk': pk})


def send_email_user(request, pk):
    content_message = request.POST['content_message']
    user_email = get_object_or_404(C4CUser, pk=pk)
    subject, from_email, to = request.POST['subject'], settings.EMAIL_HOST_USER, user_email.user.email

    htmly = get_template('email_send.html')

    d = Context({'user_to': user_email.user, 'user_that_send': request.user, 'content': content_message})
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, '', from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except SMTPDataError:
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(pk,)))
    except SMTPAuthenticationError : 
        return HttpResponseRedirect(reverse('c4c:user_detail', args=(pk,)))

    return HttpResponseRedirect(reverse('c4c:user_detail', args=(pk,)))
