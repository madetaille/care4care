from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

from c4c_app.models import C4CUser

def network(request):#, event_pk=None):
    template_name = 'network.html'
    if request.method == 'GET':
        return render_to_response(template_name, context_instance=RequestContext(request))
    
def add_user_to_network(request):#, event_pk=None):
    template_name = 'add_user_to_network.html'
    if request.method == 'GET':
        return render_to_response(template_name, context_instance=RequestContext(request))
    
    """ Edit/add an event """
    """if event_pk is not None:
        event = get_object_or_404(C4CEvent, pk=event_pk)
        if request.user != event.user:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        event = None"""

    """class ArticleForm(ModelForm):

        class Meta:
            model = C4CEvent
            fields = ['name', 'job', 'date', 'description']

    if request.method == 'POST':
        if event is not None:
            form = ArticleForm(request.POST, instance=event)
        else:
            form = ArticleForm(request.POST)
        if form.is_valid():
            # add current user and date to each entry & save
            entry = form.save(commit=False)
            print(entry.pk)
            entry.user = request.user
            entry.save()
            # form.save()
            return HttpResponseRedirect(reverse('c4c:month', args=(request.user.pk, entry.date.year, entry.date.month)))
    else:
        if event is not None:
            form = ArticleForm(instance=event)
        else:
            form = ArticleForm()
    return render(request, "network.html")#, add_csrf(request, event=event, form=form.as_table(), member=request.user))"""