from django.shortcuts import render_to_response
from django.template import RequestContext

def aboutus(request):
    """ Display the aboutus menu """
    template_name = 'about_us.html'
    if request.method == 'GET':
        return render_to_response(template_name, context_instance=RequestContext(request))