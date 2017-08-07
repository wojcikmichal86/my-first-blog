from django.conf.urls import include, url
from django.contrib.auth import views
from django.contrib import admin

urlpatterns = [
   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^academias/$', views.academias, name='academias'),
    url(r'', include('blog.urls')),

]
