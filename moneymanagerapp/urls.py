from django.conf.urls import url
from moneymanagerapp.views import CalendarView,go_to

app_name = 'cal'
urlpatterns = [

    url(r'^$', CalendarView.as_view(), name='calendar'),
    url(r'^go_to/$', go_to),
]