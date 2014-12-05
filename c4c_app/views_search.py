from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from c4c_app.models import C4CUser, C4CDonation, C4CJob
from django.views import generic

class Search(generic.ListView):
    template_name='search_result.html'
    context_object_name = 'result'
    model = C4CUser


    def get_queryset(self):
        history_list = []
        job_list = []
        user_list = []

        if 'search' in self.request.GET:
            for word_search in  str.split(self.request.GET['search']):
                job_list += list(C4CJob.objects.filter(title__icontains = word_search))
                job_list += list(C4CJob.objects.filter(description__icontains = word_search))
                job_list += list(C4CJob.objects.filter(location__icontains = word_search))
                user_list += list(User.objects.filter(last_name = word_search))
                user_list += list(User.objects.filter(first_name = word_search))
                user_list += list(User.objects.filter(username = word_search))

            print((job_list,user_list))
            job_list = set(job_list)
            user_list = set(user_list)
            history_list = [job_list, user_list]

        else:
            return HttpResponseRedirect('/')

        return (job_list,user_list)
