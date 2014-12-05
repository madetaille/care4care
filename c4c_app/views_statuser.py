from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.contrib.auth.models import User
from datetime import datetime


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num


def GraphsView(request):
    template_name='admin/stat.html'
    return render_to_response(template_name, context_instance=RequestContext(request))

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