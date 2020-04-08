from django.conf.urls import url
from moneymanagerapp.views import CalendarView,go_to,add_trans,AddView

app_name = 'cal'
urlpatterns = [
    url(r'^$', CalendarView.as_view(), name='calendar'),
    url(r'^go_to/$', go_to),
    url(r'^add_trans/',add_trans),
    url(r'^add_data/', AddView.as_view(), name='add_data'),
]