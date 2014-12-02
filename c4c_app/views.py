from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils import timezone

from c4c_app.views_user import *
from c4c_app.views_job import *
from c4c_app.views_branch import *
from c4c_app.views_donation import *
from c4c_app.views_agenda import *
from c4c_app.views_registration import *
from c4c_app.views_login import *
from c4c_app.views_stat import *

def home(request):
    return render(request,'index.html')