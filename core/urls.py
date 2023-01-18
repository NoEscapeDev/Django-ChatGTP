from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [


path('tools/',views.tools,name='tools'),
path('write/',views.write,name='write'),
path('rewrite/',views.rewrite,name='rewrite'),
path('blogideas/',views.blogideas,name='blogideas'),
path('blogoutline/',views.blogoutline,name='blogoutline'),
path('',views.login,name='login'),
path('logout/',views.logout,name='logout'),
path('download-audio/',views.Download,name='download-audio'),

]



