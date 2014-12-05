from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.contrib.auth.models import User
from c4c_app.models import C4CJob, C4CUser, C4CBranch
import datetime


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num


def GraphsView(request):
    template_name = 'admin/stat.html'


    q1 = C4CJob.objects.values_list('duration')

    number=q1.count()

    times=list(q1)

    y = np.zeros(len(times))

    for x in range (0,len(times)):
        y[x] += times[x]
    y_sum = np.cumsum(y)

    z=0
    for x in range (0,len(y_sum)):
        z += y[x]


    averagetime=z/number



    return render_to_response(template_name, {'averagetime':averagetime, }, context_instance=RequestContext(request))

def GraphsViewBar(request):

    datetimes = User.objects.values_list('date_joined', flat=True) \
                                .order_by('date_joined')
    dates = list(map(lambda d: d.date(), datetimes))

    # Get some auxilliary values
    min_date = date2num(dates[0])
    max_date = date2num(dates[-1])
    """max_date = date2num(datetime.now())"""
    days = max_date - min_date + 1

    # Initialize X and Y axes
    x = np.arange(min_date, max_date + 1)
    y = np.zeros(days)

    # Iterate over dates, increase registration array
    for date in dates:
        index = int(date2num(date) - min_date)
        y[index] += 1
    y_sum = np.cumsum(y)

    # Plot
    f = plt.figure()
    line1 = plt.plot_date(x, y_sum, xdate=True, ydate=False, ls='-', ms=0, color='#16171E')
    plt.fill_between(x, 0, y_sum, facecolor='#D0F3FF')
    plt.title('Registered Users')
    plt.rc('font', size=8)
    """
    f = plt.figure()
    x = np.arange(10)
    h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Title')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x,h,width=1.0,bottom=0,color='Green',alpha=0.65,label='Legend')
    plt.legend()"""

    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)   
    return response

def GraphsTimeworked(request):


    q2 = C4CJob.objects.values_list('duration')\
                                .order_by('start_date')


    q3 = C4CJob.objects.values_list('start_date')\
                                .order_by('start_date')

    q4 = C4CJob.objects.values_list('start_date', flat=True) \
                                .order_by('start_date')

    times = list(q2)
    dates = list(map(lambda d: d.date(), q4))

    # Get some auxilliary values
    min_date = date2num(dates[0])
    max_date = date2num(dates[-1])
    days = max_date - min_date + 1

    # Initialize X and Y axes
    x = np.arange(min_date, max_date + 1)
    y = np.zeros(days)

    # Iterate over dates, increase registration array
    count=0
    for date in dates:
        index = int(date2num(date) - min_date)
        y[index] += times[count]
        count += 1
    y_sum = np.cumsum(y)

    # Plot
    f = plt.figure()
    line1 = plt.plot_date(x, y_sum, xdate=True, ydate=False, ls='-', ms=0, color='#16171E')
    plt.fill_between(x, 0, y_sum, facecolor='#D0F3FF')
    plt.title('Time worked this year')
    plt.rc('font', size=10)

    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)
    return response

def GraphsTimeJobs(request):

    q2 = C4CJob.objects.values_list('duration')\
                                .order_by('start_date')

    q4 = C4CJob.objects.values_list('start_date', flat=True) \
                                .order_by('start_date')


    times = list(q2)
    dates = list(map(lambda d: d.date(), q4))

    # Get some auxilliary values
    min_date = date2num(dates[0])
    max_date = date2num(dates[-1])
    days = max_date - min_date + 1

    # Initialize X and Y axes
    x = np.arange(min_date, max_date + 1)
    y = np.zeros(days)

    # Iterate over dates, increase registration array
    for date in dates:
        index = int(date2num(date) - min_date)
        y[index] += 1
    y_sum = np.cumsum(y)

    # Plot
    f = plt.figure()
    line1 = plt.plot_date(x, y_sum, xdate=True, ydate=False, ls='-', ms=0, color='#16171E')
    plt.fill_between(x, 0, y_sum, facecolor='#D0F3FF')
    plt.title('Jobs done')
    plt.rc('font', size=10)

    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)
    return response

def ActivePie(request):

    useractive = User.objects.filter(is_active=True)
    nuseractive=len(useractive)
    userstot= User.objects.count()

    x= [nuseractive,userstot-nuseractive]

    # Plot
    f = plt.figure()
    line1 = plt.pie(x, explode=None, labels=['Active', 'Inactive'], colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'), autopct=None, pctdistance=0.6, shadow=False, labeldistance=1.1, startangle=None, radius=None)
    plt.title('Active and inactive users')
    plt.rc('font', size=18)


    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)
    return response

def UserByBranch(request):

    userbybranchs=[]

    q1=C4CBranch.objects.values_list('group')\
                                .order_by('group')
    max=0
    for x in q1:
        q2=User.objects.filter(groups__in=(x))
        userbybranchs.append(len(q2))
        if max < len(q2):
            max = len(q2)

    namebranchs=[]
    q3=C4CBranch.objects.values_list('name')\
                                .order_by('group')
    for x in q3:
        namebranchs.append(x)

    f = plt.figure()
    x = np.arange(len(q1))
    width=0.5
    plt.xlim(0, len(q1)+2)
    plt.ylim(0, max+2)
    plt.title('Number of users by branch')
    plt.xlabel('branch name')
    plt.ylabel('number of users')
    bar1 = plt.bar(x,userbybranchs, width, bottom=0, color='Green', alpha=0.65, label='Legend')
    plt.xticks(x+width/2., namebranchs)
    plt.rc('font', size=12)



    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)
    return response