from django.http import HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.template import RequestContext

def news(request):
    data = [['100',10],['90',9],['80',8]]
    template_name = 'news.html'
    if request.method == 'GET':
        '''return render(request, template_name)'''

        return render_to_response(template_name, {
                                            'data': data,
                                            },
                                            context_instance=RequestContext(request))