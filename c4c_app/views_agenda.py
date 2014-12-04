import calendar
from datetime import date, timedelta
import time

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from c4c_app.models import C4CEvent, C4CUser
mnames = "January February March April May June July August September October November December"
mnames = mnames.split()


def _get_monthes_for_year(member, year):
    nowy, nowm = time.localtime()[:2]

    mlst = []
    for n, month in enumerate(mnames):
        current = False   # are there entry(s) for this month; current month?
        entries = C4CEvent.objects.filter(date__year=year, date__month=n + 1, user=member.user)

        if year == nowy and n + 1 == nowm:
            current = True

        mlst.append(dict(n=n + 1, name=month, nb_entry=len(entries), entries=entries, current=current))
    return mlst


def year(request, member_pk=None, year=None):
    """Main listing, years and months; three years per page."""
    # prev / next years
    member = None
    if member_pk:
        member = get_object_or_404(C4CUser, pk=member_pk)
    else:
        member = get_object_or_404(C4CUser, user=request.user)

    if member != request.user.c4cuser and not member.network.filter(pk=request.user.pk).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')

    if year:
        year = int(year)
    else:
        year = time.localtime()[0]

    # create a list of months for each year, indicating ones that contain entries and current
    mlst = _get_monthes_for_year(member, year)

    has_entries = False
    for month in mlst:
        if len(month["entries"]) != 0:
            has_entries = True

    context = {'months': mlst, 'member': member, 'year': year, 'has_entries': has_entries}

    return render(request, "agenda.html", context)


def month(request, member_pk, year, month, change=None):
    """Listing of days in `month`."""

    member = None
    if member_pk:
        member = get_object_or_404(C4CUser, pk=member_pk)
    else:
        member = get_object_or_404(C4CUser, user=request.user)

    if member != request.user.c4cuser and not member.network.filter(pk=request.user.pk).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')

    year, month = int(year), int(month)

    # apply next / previous change
    if change in ('next', 'prev'):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == 'next':
            mod = mdelta
        elif change == 'prev':
            mod = -mdelta

        year, month = (now + mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    mlst = _get_monthes_for_year(member, year)

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    for day in month_days:
        entries = []
        current = False   # are there entries for this day; current day?
        if day:
            entries = C4CEvent.objects.filter(date__year=year, date__month=month, date__day=day, user=member.user)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    context = {'year': year, 'months': mlst, 'month': month, 'member': member, 'month_days': lst, 'mname': mnames[month - 1]}

    return render(request, "month.html", context)


def day(request, member_pk, year, month, day):
    member = None
    if member_pk:
        member = get_object_or_404(C4CUser, pk=member_pk)
    else:
        member = get_object_or_404(C4CUser, user=request.user)

    if member != request.user.c4cuser and not member.network.filter(pk=request.user.pk).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')

    year, month, day = int(year), int(month), int(day)
    day_name = date(year, month, day).strftime("%A")
    month_name = mnames[month - 1]
    entries = C4CEvent.objects.filter(date__year=year, date__month=month, date__day=day, user=member.user)

    context = {'year': year, 'month': month, 'day': day, 'member': member, 'month_name': month_name, 'day_name': day_name, 'entries': entries}

    return render(request, "day.html", context)


def event(request, event_pk):
    event = get_object_or_404(C4CEvent, pk=event_pk)
    if event.user != request.user and not event.user.c4cuser.network.filter(pk=request.user.pk).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    context = {"event": event}
    return render(request, "event.html", context)


def edit_event(request, event_pk=None):
    """ Edit/add an event """
    if event_pk is not None:
        event = get_object_or_404(C4CEvent, pk=event_pk)
        if request.user != event.user:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        event = None

    class ArticleForm(ModelForm):

        class Meta:
            model = C4CEvent
            fields = ['name', 'job', 'date', 'description']

    if request.method == 'POST':
        if event is not None:
            form = ArticleForm(request.POST, instance=event)
        else:
            form = ArticleForm(request.POST)
        if form.is_valid():
            # add current user and date to each entry & save
            entry = form.save(commit=False)
            print(entry.pk)
            entry.user = request.user
            entry.save()
            # form.save()
            return HttpResponseRedirect(reverse('c4c:month', args=(request.user.pk, entry.date.year, entry.date.month)))
    else:
        if event is not None:
            form = ArticleForm(instance=event)
        else:
            form = ArticleForm()
    return render(request, "edit_event.html", add_csrf(request, event=event, form=form.as_table(), member=request.user))


@login_required
def add_csrf(request, ** kwargs):
    """Add CSRF and user to dictionary."""
    d = dict(** kwargs)
    d.update(csrf(request))
    return d
