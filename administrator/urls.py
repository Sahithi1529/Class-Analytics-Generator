from django.urls import path
from . import views
urlpatterns = [
   path("",views.Login), # Request @/administrator/
   path('admin-dashboard',views.adminDashboard), # Request @/administrator/admin-dashboard
   path("download-data",views.downloadData), # Request @/administrator/download-data?download-what
   path('logout',views.logout), # Request @/administrator/logout  - done
   path('view-messages',views.viewMessages), # Request @/administrator/view-messages - done
   path('send-message',views.sendMessage), # Request @/administrator/send-message - done
   path('view-faculty',views.viewFaculty),
   path('update-manually',views.updateManually), # Request @/administrator/update-manually - done
   path('update-model',views.updateModel),
   path('updatethem',views.updateThem), # Done
   path('update-password',views.updatePassword), #Done
   path('manage-database',views.manageDatabase),
   path("add-via-csv",views.addViaCSV), # Done,
   path("generate-analytics",views.generateAnalytics)


# Update admin dashboard
# Should add Button to download data
# Generate Analytics in admin 
# Front end for Manage database
# 


]
