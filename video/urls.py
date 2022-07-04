from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path('home/<cf>', views.HomeViewSet.as_view({'get':'home_list'})), #cf 为分类左至右 0 1 2 3
    #path('search/<int:type>', views.HomeViewSet.as_view({'post':'search_list'}), name='search'), #0 播放高 1 点赞高  默认为播放高
   # path('detail/<int:pk>', views.HomeViewSet.as_view({'get':'detail'})),
    path('detail/<int:pk>', views.detail),
    path('search/<int:type>', views.search_list),
    path('like/', views.like, name='like'),
    path('collect/', views.collect, name='collect'),
    path('publish/', views.publish, name='publish'),
    path('attention/', views. attention),
]