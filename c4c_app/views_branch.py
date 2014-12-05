from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from c4c_app.models import C4CBranch

class BranchDetail(generic.DetailView):
    model = C4CBranch
    template_name = 'branch_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BranchDetail, self).get_context_data(**kwargs)

        c4cuser = get_object_or_404(C4CUser, user=self.request.user)
        context['c4cuser'] = c4cuser
        return context
