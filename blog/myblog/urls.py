from django.contrib import admin
from django.urls import path, include,re_path
from myblog import views
from myblog.RSS import PostFeed


# 设置命名空间需要加上 app_name
app_name = 'myblog'
urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    re_path('detail/(?P<pk>\d*)', views.Detail.as_view(), name='detail'),

    # path('achives/', views.Archives.as_view(), name='archives'),
]
