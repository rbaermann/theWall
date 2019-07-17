from django.conf.urls import url
from . import views
                
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg$', views.reg),
    url(r'^login$', views.log),
    url(r'^wall$', views.wall),
    url(r'^logout$', views.logout),
    url(r'^wall/createMessage$', views.createMessage),
    url(r'^message/(?P<messageId>\d+)/destroy$', views.deleteMessage),
    url(r'^comment/(?P<messageId>\d+)/create$', views.createComment),
]