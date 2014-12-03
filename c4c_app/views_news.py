from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from c4c_app.models import C4CNews, C4CUser, C4CBranch
from datetime import *
from django.views import generic
from django import forms

class NewsCreation(CreateView):


    fields = [ 'title', 'branch', 'description']
    model = C4CNews
    template_name = 'news_form.html'
    #description = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        success_url = '/news_detail/'
        #branch = get_object_or_404(C4CBranch, self.request.POST['branch'] )

        self.object.title = self.request.POST['title']
        self.object.user = get_object_or_404(C4CUser, user=self.request.user).user
        self.object.date = datetime.now()
        self.object.description = self.request.POST['description']
        #self.object.branch = branch
        self.object.save()

        return HttpResponseRedirect(reverse("c4c:news_detail", args=(self.object.id,)))



class NewsDetail(generic.DetailView):
    model = C4CNews
    template_name = 'news_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NewsDetail, self).get_context_data(**kwargs)
        # Add in the publisher
        #member = get_object_or_404(C4CNews, user=self.request.user.user)
        #context['News'] = member
        return context

class AllNews(generic.ListView):
    template_name = 'all_news.html'
    context_object_name = 'allNews'
    model = C4CNews

    def get_queryset(self):
        allNews = C4CNews.objects.order_by('-date')

        return allNews

class AllNewsBranch(generic.ListView):
    template_name = 'all_news.html'
    context_object_name = 'allNews'
    model = C4CNews

    def get_queryset(self):
        #member = get_object_or_404(C4CUser, user=self.request.user)
        #allNews = C4CNews.objects.filter(branch = member.branches)
        allNews = []
        return allNews