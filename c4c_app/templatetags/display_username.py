from django import template
from django.core.urlresolvers import reverse
from django.utils.html import escape
from c4c_app.models import C4CBranch
register = template.Library()


@register.simple_tag
def display_username(user, link=True):
    """ Display a user with a link to its profile """
    if user is None:
        return "Nobody"

    if user.is_superuser:
        color = '#F00'
    elif len(user.c4cuser.get_administrated_branches()) != 0:
        color = '#00F'
    elif C4CBranch.objects.filter(main_user=user).exists():
        color = "#0F0"
    else:
        color = '#000'
    if link:
        link = reverse('c4c:user_detail', args=(user.pk,))
        return "<a href='" + link + "' style='color:" + color + "'>" + escape(user.first_name + " " + user.last_name) + "</a>"
    else:
        return "<span style='color:" + color + "'>" + escape(user.first_name + " " + user.last_name) + "</span>"
