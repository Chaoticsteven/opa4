from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('like_videos/', views.like_list,name='like_list'),
    path('collect_videos/', views.collect_list, name='collect_videos'),
    path('create_videos/', views.create_list ,name='create_videos'),
    path('attention/', views.attention_list, name='attention_users'),
    path('', views.get_like_count),
    path('other_user/<int:pk>', views.create_list2),
]
