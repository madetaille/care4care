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
        job_list_no_redundumcy = []
        user_list_no_redundumcy = []
        #donations_sent = []
        #donation_received = []
        #job_demanded = []
        #job_done = []

        if 'search' in self.request.GET:
            for word_search in  str.split(self.request.GET['search']):
                job_title = C4CJob.objects.filter(title__icontains = word_search)
                job_list.append(job_title)
            for word_search in  str.split(self.request.GET['search']):
                job_description = C4CJob.objects.filter(description__icontains = word_search)
                job_list.append(job_description)
            for word_search in  str.split(self.request.GET['search']):
                job_location = C4CJob.objects.filter(location__icontains = word_search)
                job_list.append(job_location)
            for word_search in  str.split(self.request.GET['search']):
                user_lastname = User.objects.filter(last_name = word_search)
                user_list.append(user_lastname)
            for word_search in  str.split(self.request.GET['search']):
                user_first_name = User.objects.filter(first_name = word_search)
                user_list.append(user_first_name)

            if job_list:
                for i in job_list:
                    for j in i:
                        if j not in job_list_no_redundumcy:
                            job_list_no_redundumcy.append(j)
                history_list.append(job_list_no_redundumcy)
            if user_list:
                for i in user_list:
                    for j in i:
                        if j not in user_list_no_redundumcy:
                            user_list_no_redundumcy.append(j)
                history_list.append(user_list_no_redundumcy)

        else:
            return HttpResponseRedirect("/")



        return history_list