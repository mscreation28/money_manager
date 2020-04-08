from datetime import datetime, timedelta
from calendar import HTMLCalendar
from moneymanagerapp.models import Data


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day ,data):
        trans_per_day = data.filter(day__day=day)
        d = ''
        count=0
        for data in trans_per_day:
            if(data.check==0):
                d += f'<li> - {data.amount}:{data.notes} </li>'
                count-=data.amount
            else:
                d += f'<li> + {data.amount}:{data.notes} </li>'
                count+=data.amount
        
        if(d!=''):
            d+= f'---------<br>'
            d+= f'Total = {count}'

        if day != 0:
            return f"<td><a href='add_data?day={day}&type=0'><span class='date'>{day}</span><ul>{d}</ul></a></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek,data):
        week=''
        for d, weekday in theweek:
            week+=self.formatday(d,data)
        return f'<tr> {week} </tr>'
       

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        # events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
        data = Data.objects.filter(day__year=self.year, day__month=self.month)
        count=0
        count1=0
        for datas in data:
            if(datas.check==0):
                count+=datas.amount
            else:
                count1+=datas.amount

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'Debit : {count} \t Credit : {count1} \t Total : {count1-count}'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week,data)}\n'
        return cal