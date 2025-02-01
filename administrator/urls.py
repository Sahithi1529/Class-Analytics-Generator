from django.urls import path
from . import views
urlpatterns = [
   path("",views.Login),
   path('test',views.Test),
   path("download-data",views.DownloadData)
]
