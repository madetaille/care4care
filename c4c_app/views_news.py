
from django.shortcuts import get_object_or_404
from django.views import generic

from c4c_app.models import C4CNews, C4CUser


class AllNews(generic.ListView):
    template_name = 'all_news.html'
    context_object_name = 'allNews'
    model = C4CNews

    def get_queryset(self):
        allNews = C4CNews.objects.order_by('-date')
        return allNews

    def get_context_data(self, **kwargs):
        context = super(AllNews, self).get_context_data(**kwargs)
        context['all'] = True
        return context


class AllNewsBranch(generic.ListView):
    template_name = 'all_news.html'
    context_object_name = 'allNews'
    model = C4CNews

    def get_queryset(self):
        allNews = []
        user = get_object_or_404(C4CUser, user=self.request.user)
        branches = user.get_branches()

        for one_branch in branches:
            allNews += C4CNews.objects.filter(branch=one_branch.name)

        allNews.sort(key=lambda x: x.date, reverse=True)  # sorted by date
        return allNews

    def get_context_data(self, **kwargs):
        context = super(AllNewsBranch, self).get_context_data(**kwargs)
        context['all'] = False
        return context
