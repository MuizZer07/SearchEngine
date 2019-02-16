from django.conf.urls import url
from .views import HomeView
from . import views

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
] 
