from django.urls import path
from . import views
urlpatterns = [
   path("",views.Login), # Request @/administrator/
   path('test',views.Test), # Test URL to test
   path("download-data",views.downloadData), # Request @/administrator/download-data
   path("add-faculty-via-csv",views.addFacultyViaCSV), # Request POST @/administrator/add-faculty-via-csv
   path("add-admin-via-csv",views.addAdminViaCSV), # Request POST @/administrator/add-admin-via-csv
   path('admin-dashboard',views.adminDashboard), # Request @/administrator/admin-dashboard
   path('logout',views.logout), # Request @/administrator/logout
   path('update-model',views.updateModel),
    path('view-messages',views.viewMessages),
    path('send-message',views.sendMessage),
    path('view-faculty',views.viewFaculty),



]
