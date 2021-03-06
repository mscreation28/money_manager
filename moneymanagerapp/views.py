from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import calendar
from django.conf import settings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from moneymanagerapp.models import Data
from moneymanagerapp.calander import Calendar
from moneymanagerapp.forms import UserRegisterForm

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

        cal = Calendar(d.year, d.month ,self.request.user.id)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['today'] = datetime.today().month
        context['date'] = d
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        data=Data.objects.filter(day__month=d.month, day__year=d.year, user=self.request.user.id)

        x=[get_cFood(data),get_cEducation(data),get_cTransport(data),get_cOther(data)]   
        labels=["Food","Education","Transport","Other"]
        plt.pie(x,labels=labels,autopct='%1.1f%%')
        plt.title("Expense", fontsize=20)
        plt.legend()
        # plt.savefig('moneymanagerapp/static/img/fig.png')
        plt.savefig('/home/mscreation028/mscreation028.pythonanywhere.com/static/img/fig.png')
        plt.close()

        x=[get_cCash(data),get_cCard(data),get_cSalary(data),get_cOthers(data)]   
        labels=["Cash","Card","Salary","Other"]
        plt.pie(x,labels=labels,autopct='%1.1f%%')
        plt.title("Income", fontsize=20)
        plt.legend()
        # plt.savefig('moneymanagerapp/static/img/fig1.png')
        plt.savefig('/home/mscreation028/mscreation028.pythonanywhere.com/static/img/fig1.png')
        plt.close()

        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)

        # request.user.id=self.request.user.id
        
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
    url='/home/?month='
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
    u = User.objects.get(id = request.user.id)
    data=Data()
    data.user=u
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

        data=Data.objects.filter(day__month=d.month, day__year=d.year, user=self.request.user.id)
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

        data=Data.objects.filter(day__month=d.month, day__year=d.year, user=self.request.user.id)
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
        context['data']=Data.objects.filter(day=add_date , user=self.request.user.id)
        context['add_date'] = add_date
        
        data=Data.objects.filter(day__month=d.month, day__year=d.year, user=self.request.user.id)
        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)
        
        return context

def delete_data(request):
    did=int(request.GET['id'])
    instance = Data.objects.get(id=did,user=request.user.id)
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
        instance = Data.objects.get(id=eid, user=self.request.user.id)

        add_date=datetime(d.year,d.month,int(self.request.GET['day']))
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['data']=Data.objects.filter(day=add_date, user=self.request.user.id)
        context['flag']=1
        context['instance']=instance
        # print(instance)
        context['add_date'] = add_date
        
        data=Data.objects.filter(day__month=d.month, day__year=d.year, user=self.request.user.id)
        context['expense']=get_expense(data)
        context['income']=get_income(data)
        context['available']=get_income(data)-get_expense(data)
        
        return context

def edit_data_db(request):
    did=int(request.GET['id'])
    instance = Data.objects.get(id=did, user=request.user.id)

    instance.amount=request.POST['amount']
    instance.notes=request.POST['note']
    instance.day=request.POST['adate']
    instance.etype=request.POST['etype']
    instance.save()

    url="/show_data?day="
    url+=request.GET['day']
    return HttpResponseRedirect(url)



def login(request):
    c = {}
    c.update(csrf(request))
    
    return render(request,'login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    request.session['password']=password
    
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        
        auth.login(request, user)
        return HttpResponseRedirect('/home')
    else:
        messages.add_message(request,messages.WARNING,'Invalid Login Details')
        return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)       
        if form.is_valid():     
            form.save()    
            messages.add_message(request,messages.SUCCESS, 'Profile details updated.')
            return render(request,'login.html')
    else:
        form=UserRegisterForm()
    return render(request,'signup.html',{'form':form})


@login_required(login_url='/login')

def logout_request(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS, 'Logged-out Successfully')
    return render(request,'login.html')