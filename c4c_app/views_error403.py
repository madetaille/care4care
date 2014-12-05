from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.template.loader import get_template


def error403(request):
    template403 = get_template('error403.html')
    context = RequestContext(request, {})
    return HttpResponseForbidden(template403.render(context))
