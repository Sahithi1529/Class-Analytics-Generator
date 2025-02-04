from django.urls import path
from . import views
urlpatterns = [
   path("",views.Login), # Request @/administrator/
   path('test',views.Test), # Test URL to test
   path("download-data",views.downloadData), # Request @/administrator/download-data
   path("add-data-via-csv",views.addDataViaCSV), # Request POST @/administrator/add-data-via-csv
   path('admin-dashboard',views.adminDashboard), # Request @/administrator/admin-dashboard
   path('logout',views.logout), # Request @/administrator/logout
   path('update-model',views.updateModel)

]
