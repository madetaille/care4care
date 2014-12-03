from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def aboutus(request):
    #return render_to_response('what_is_c4c.html')
    template_name = 'about_us.html'
    if request.method == 'GET':
        return render_to_response(template_name, context_instance=RequestContext(request))