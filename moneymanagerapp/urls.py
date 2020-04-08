from django.conf.urls import url
from moneymanagerapp.views import CalendarView,go_to,add_trans,AddView,Add1View,ShowView,delete_data,EditView,edit_data_db

app_name = 'cal'
urlpatterns = [
    url(r'^$', CalendarView.as_view(), name='calendar'),
    url(r'^go_to/$', go_to),
    url(r'^add_trans/',add_trans),
    url(r'^add_data/', AddView.as_view(), name='add_data'),
    url(r'^add_data_inc/', Add1View.as_view(), name='add_data_inc'),
    url(r'^show_data/',ShowView.as_view(), name='show_data'),
    url(r'^delete_data/',delete_data, name='delete_data'),
    url(r'^edit_data/',EditView.as_view(), name='edit_data'),
    url(r'^edit_data_db/',edit_data_db, name='edit_data_db'),
]