from django.urls import path
from . import views



app_name = 'myadmin'
urlpatterns = [
    path('adminlogin/', views.login, name='login'),
    path('adminlogout/', views.logout, name='logout'),
    path('audit_list/',views.audit_list, name='audit'),
    path('complaint_list/',views.complaint_list, name='audit'),
    path('auditpass/', views.auditpass),
    path('auditnopass/', views.auditnopass),
]

