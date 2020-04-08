from django.conf.urls import url
from moneymanagerapp.views import CalendarView,go_to,add_trans,AddView,Add1View

app_name = 'cal'
urlpatterns = [
    url(r'^$', CalendarView.as_view(), name='calendar'),
    url(r'^go_to/$', go_to),
    url(r'^add_trans/',add_trans),
    url(r'^add_data/', AddView.as_view(), name='add_data'),
    url(r'^add_data_inc/', Add1View.as_view(), name='add_data'),
]