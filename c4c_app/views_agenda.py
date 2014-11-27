from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from django.utils import timezone
from datetime import date, datetime, timedelta
import calendar
import time

from c4c_app.models import C4CEvent, C4CUser, C4CJob

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

def year(request, year=None, member_pk=None):
    """Main listing, years and months; three years per page."""
    # prev / next years
    
    member=None
    if member_pk: member = get_object_or_404(C4CUser, pk=member_pk)
    else: member = get_object_or_404(C4CUser, user=request.user)
    
    if year: year = int(year)
    else:    year = time.localtime()[0]

    nowy, nowm = time.localtime()[:2]
    lst = []

    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year]:
        mlst = []
        for n, month in enumerate(mnames):
            entry = current = False   # are there entry(s) for this month; current month?
            entries = C4CEvent.objects.filter(date__year=y, date__month=n+1, user=member)

            if entries:
                entry = True
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
        lst.append((y, mlst))

    return render_to_response("agenda.html", dict(years=lst, user=member, year=year))

def month(request, year, month, change=None, member_pk=None):
    
    member=None
    if member_pk: member = get_object_or_404(C4CUser, pk=member_pk)
    else: member = get_object_or_404(C4CUser, user=request.user)
    
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    # apply next / previous change
    if change in ('next', 'prev'):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == 'next':   mod = mdelta
        elif change == 'prev': mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    for day in month_days:
        entries = current = False   # are there entries for this day; current day?
        if day:
            entries = C4CEvent.objects.filter(date__year=year, date__month=month, date__day=day, user=member)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render_to_response("month.html", dict(year=year, month=month, user=member,
                        month_days=lst, mname=mnames[month-1]))
    
def day(request, year, month, day, member_pk=None):
    
    member=None
    if member_pk: member = get_object_or_404(C4CUser, pk=member_pk)
    else: member = get_object_or_404(C4CUser, user=request.user)
    
    change =(member.user == request.user)
    
    """Entries for the day."""
    EntriesFormset = modelformset_factory(C4CEvent, extra=1, exclude=("user", "date"),
                                          can_delete=True)

    if request.method == 'POST':
        formset = EntriesFormset(request.POST)
        if formset.is_valid():
            # add current user and date to each entry & save
            entries = formset.save(commit=False)
            for entry in entries:
                entry.user = get_object_or_404(C4CUser, user=member.user)
                entry.date = date(int(year), int(month), int(day))
                entry.save()
            return HttpResponseRedirect(reverse('c4c:month', args=(year, month, member.pk)))

    else:
        # display formset for existing enties and one extra form
        formset = EntriesFormset(queryset=C4CEvent.objects.filter(date__year=year,
            date__month=month, date__day=day, user=member))
    return render_to_response("day.html", add_csrf(request, entries=formset, year=year,
            month=month, day=day))


def add_csrf(request, ** kwargs):
    """Add CSRF and user to dictionary."""
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d
