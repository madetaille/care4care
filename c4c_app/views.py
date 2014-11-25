from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils import timezone

from c4c_app.models import *
from c4c_app.views_user import *
from c4c_app.views_job import *