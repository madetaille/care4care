from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User

from c4c_app.models import C4CUser

class UserDetail(generic.DetailView):
	model = C4CUser
	template_name = 'user_detail.html'
    
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(UserDetail, self).get_context_data(**kwargs)
		viewer = get_object_or_404(C4CUser, user=self.request.user)
		context['viewer'] = viewer
		return context

class UserEdit(generic.edit.UpdateView):
	model = C4CUser
	fields = ['address', 'birthday']
	template_name= 'c4cuser_edit.html'
		
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.save()
		return HttpResponseRedirect(reverse('c4c:user_detail', args=(self.object.pk,)))
        
class PersonalNetwork(generic.ListView):
    template_name = 'network.html'
    context_object_name = 'network_list'
    
    def get_queryset(self):
        member = get_object_or_404(C4CUser, user=self.request.user)
        return member.network.all()
