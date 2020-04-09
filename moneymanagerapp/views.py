from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.conf import settings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from moneymanagerapp.models import Data
from moneymanagerapp.calander import Calendar

class CalendarView(generic.ListView):
    model = Data
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))

        cmonth=str(d.year)
        cmonth+='-'
        cmonth+=str(d.month)
        self.request.session['cmonth']=cmonth

        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['today'] = datetime.today().month
        context['date'] = d
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        data=Data.objects.filter(day__month=d.month)

        x=[get_cFood(data),get_cEducation(data),get_cTransport(data),get_cOther(data)]   
        labels=["Food","Education","Transport","Other"]
        plt.pie(x,labels=labels,autopct='%1.1f%%')
        plt.title("Expense", fontsize=20)
        plt.legend()
        plt.savefig('home/mscreation028/mscreation028.pythonanywhere.com/static/img/fig.png')
        plt.close()

        x=[get_cCash(data),get_cCard(data),get_cSalary(data),get_cOthers(data)]   
        labels=["Cash","Card","Salary","Other"]
        plt.pie(x,labels=labels,autopct='%1.1f%%')
        plt.title("Income", fontsize=20)
        plt.legend()
        plt.savefig('home/mscreation028/mscreation028.pythonanywhere.com/static/img/fig1.png')
        plt.close()

        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)
        
        return context

def get_expense(data):
    ex=0
    for datas in data:
        if(datas.check==0):
            ex+=datas.amount
    return ex

def get_income(data):
    ic=0
    for datas in data:
        if(datas.check==1):
            ic+=datas.amount
    return ic

def get_cFood(data):
    cFood=0
    for datas in data:
        if(datas.etype=="Food"):
            cFood+=datas.amount
    return cFood

def get_cEducation(data):
    cEducation=0
    for datas in data:    
        if(datas.etype=="Education"):
            cEducation+=datas.amount
    return cEducation

def get_cTransport(data):
    cTransport=0
    for datas in data:
        if(datas.etype=="Transport"):
            cTransport+=datas.amount
    return cTransport

def get_cOther(data):
    cOther=0
    for datas in data:
        if(datas.etype=="Other"):
            cOther+=datas.amount
    return cOther

def get_cCard(data):
    cCard=0
    for datas in data:
        if(datas.etype=="Card"):
            cCard+=datas.amount
    return cCard

def get_cCash(data):
    cCash=0
    for datas in data:        
        if(datas.etype=="Cash"):
            cCash+=datas.amount
    return cCash

def get_cSalary(data):
    cSalary=0
    for datas in data:            
        if(datas.etype=="Salary"):
            cSalary+=datas.amount
    return cSalary

def get_cOthers(data):
    cOthers=0
    for datas in data:            
        if(datas.etype=="Others"):
            cOthers+=datas.amount
    return cOthers

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
    data.etype=request.POST['etype']
    data.time=datetime.now().time()
    if(request.GET['type']=='1'):
        data.check=1
    else:
        data.check=0
    data.save()

    tdate=request.POST['adate']
    print(tdate)
    sdate=tdate.split('-')
    url="/show_data?day="
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

        add_date=datetime(d.year,d.month,int(self.request.GET['day']))
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['today'] = datetime.today().month
        context['date'] = d
        context['add_date'] = add_date
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        data=Data.objects.filter(day__month=d.month)
        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)
        return context
    # return render(request,'add_data.html')

class Add1View(generic.ListView):
    model = Data
    template_name = 'add_data_inc.html'
    # print(request.GET['day'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.session['cmonth'])
        cal = Calendar(d.year, d.month)

        add_date=datetime(d.year,d.month,int(self.request.GET['day']))
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['today'] = datetime.today().month
        context['date'] = d
        context['add_date'] = add_date
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        data=Data.objects.filter(day__month=d.month)
        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)
        
        return context

class ShowView(generic.ListView):
    model = Data
    template_name = 'show_data.html'
    # print(request.GET['day'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.session['cmonth'])
        cal = Calendar(d.year, d.month)

        add_date=datetime(d.year,d.month,int(self.request.GET['day']))
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['data']=Data.objects.filter(day=add_date)
        context['add_date'] = add_date
        
        data=Data.objects.filter(day__month=d.month)
        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)
        
        return context

def delete_data(request):
    did=int(request.GET['id'])
    instance = Data.objects.get(id=did)
    instance.delete()
    url="/show_data?day="
    url+=request.GET['day']
    return HttpResponseRedirect(url)

class EditView(generic.ListView):
    model = Data
    template_name = 'edit_data.html'
    # print(request.GET['day'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.session['cmonth'])
        cal = Calendar(d.year, d.month)

        eid=int(self.request.GET['id'])
        instance = Data.objects.get(id=eid)

        add_date=datetime(d.year,d.month,int(self.request.GET['day']))
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['data']=Data.objects.filter(day=add_date)
        context['flag']=1
        context['instance']=instance
        # print(instance)
        context['add_date'] = add_date
        
        data=Data.objects.filter(day__month=d.month)
        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)
        
        return context

def edit_data_db(request):
    did=int(request.GET['id'])
    instance = Data.objects.get(id=did)

    instance.amount=request.POST['amount']
    instance.notes=request.POST['note']
    instance.day=request.POST['adate']
    instance.etype=request.POST['etype']
    instance.save()

    url="/show_data?day="
    url+=request.GET['day']
    return HttpResponseRedirect(url)

