from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from moneymanagerapp.models import Data
from moneymanagerapp.calander import Calendar

class CalendarView(generic.ListView):
    model = Data
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = get_date(self.request.GET.get('month', None))
        # try:
        #     d=get_date(self.request.session['cmonth'])
        # except:
        d = get_date(self.request.GET.get('month', None))
            # self.request.session['month']=self.request.GET['month']

        cmonth=str(d.year)
        cmonth+='-'
        cmonth+=str(d.month)
        self.request.session['cmonth']=cmonth

        print(cmonth)
        
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['today'] = datetime.today().month
        context['date'] = d
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def go_to(request):
    tdate=request.POST['tdate']
    print(tdate)
    sdate=tdate.split('-')
    url='/?month='
    url+=str(sdate[0])
    url+='-'
    url+=str(sdate[1])
    cmonth=str(sdate[0])
    cmonth+='-'
    cmonth+=str(sdate[1])
    print(cmonth)
    request.session['cmonth']=cmonth
    return HttpResponseRedirect(url)

def add_trans(request):
    data=Data()
    data.amount=request.POST['amount']
    data.notes=request.POST['note']
    data.day=request.POST['adate']
    data.time=datetime.now().time()
    if(request.POST['type']=="Income"):
        data.check=1
    else:
        data.check=0
    data.save()

    tdate=request.POST['adate']
    print(tdate)
    sdate=tdate.split('-')
    url="/add_data?day="
    url+=str(sdate[2])

    return HttpResponseRedirect(url)

class AddView(generic.ListView):
    model = Data
    template_name = 'add_data.html'
    # print(request.GET['day'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.session['cmonth'])
        cal = Calendar(d.year, d.month)
        print(d.month)
        print(d.year)
        add_date=datetime(d.year,d.month,int(self.request.GET['day']))
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['today'] = datetime.today().month
        context['date'] = d
        context['add_date'] = add_date
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    # return render(request,'add_data.html')