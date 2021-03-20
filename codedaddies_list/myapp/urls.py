from django.urls import path
from .views import index,newsearch
urlpatterns = [
    path("",index ,name='home'),
    path("newsearch/",newsearch)
]
