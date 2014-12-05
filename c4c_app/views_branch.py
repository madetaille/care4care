from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import ListView

from c4c_app.models import C4CBranch
class BranchDetail(generic.DetailView):

    """ Display branch details """
    model = C4CBranch
    template_name = 'branch_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BranchDetail, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            context['user'] = self.request.user

        context['pk'] = self.kwargs.get('pk')
        return context


def add_to_branch(request, pk):
    ''' Add request.user to branch pk '''
    c4cbranch = get_object_or_404(C4CBranch, pk=pk)
    c4cbranch.group.user_set.add(request.user)
    return HttpResponseRedirect(reverse('c4c:branch_detail', args=(pk,)))


def remove_from_branch(request, pk):
    """ Remove a user from a branch """
    c4cbranch = get_object_or_404(C4CBranch, pk=pk)
    c4cbranch.group.user_set.remove(request.user)
    return HttpResponseRedirect(reverse('c4c:branch_detail', args=(pk,)))


class BranchList(ListView):

    """ Desplay branches List """
    model = C4CBranch
    template_name = 'branchlist.html'
    context_object_name = 'all_branches'
