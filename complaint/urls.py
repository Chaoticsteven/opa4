from django.urls import path
from . import views

app_name = 'complaint'
urlpatterns = [
    path('submit_complaint/<int:pk>',views.submit_complaint, name='submit_complaint'),
]