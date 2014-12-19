from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic

from c4c_app.models import C4CUser, C4CDonation, C4CJob
class Search(generic.ListView):
    template_name = 'search_result.html'
    context_object_name = 'result'
    model = C4CUser

    def get_queryset(self):
        job_list = []
        user_list1 = []
        user_list2 = []
        user_list3 = []
        user_list = []

        if 'search' in self.request.GET:
            for word_search in str.split(self.request.GET['search']):
                job_list += list(C4CJob.objects.filter(title__icontains=word_search))
                job_list += list(C4CJob.objects.filter(description__icontains=word_search))
                job_list += list(C4CJob.objects.filter(location__icontains=word_search))
                user_list1 += list(User.objects.filter(last_name__icontains=word_search))
                user_list2 += list(User.objects.filter(first_name__icontains=word_search))
                user_list3 += list(User.objects.filter(username__icontains=word_search))

                for i in user_list1:
                    user_list.append(i)

                for i in user_list2:
                    user_list.append(i)

                for i in user_list3:
                    user_list.append(i)

            job_list = set(job_list)
            user_list = set(user_list)

        else:
            return HttpResponseRedirect('/')

        return (job_list, user_list)


class SearchNetwork(generic.ListView):
    template_name = 'search_result_network.html'
    context_object_name = 'result'
    model = C4CUser

    def get_queryset(self):
        user_list = []
        user_list_1 = []
        user_list_2 = []
        user_list_3 = []
        user = get_object_or_404(C4CUser, user=self.request.user)
        if 'search' in self.request.GET:
            for word_search in str.split(self.request.GET['search']):

                user_list_1 += list(User.objects.filter(last_name__icontains=word_search))
                user_list_2 += list(User.objects.filter(first_name__icontains=word_search))
                user_list_3 += list(User.objects.filter(username__icontains=word_search))

                for i in user_list_1:
                    if i.pk != user.pk:
                        user_list.append(i)

                for i in user_list_2:
                    if i.pk != user.pk:
                        user_list.append(i)

                for i in user_list_3:
                    if i.pk != user.pk:
                        user_list.append(i)

            user_list = set(user_list)

        else:
            return HttpResponseRedirect('/')

        return user_list
