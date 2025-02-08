from django.urls import path
from . import views
urlpatterns = [
    path('',views.facultyLogin), #Request @/faculty
    path("faculty-dashboard",views.facultyDashboard), #Request @/faculty/faculty-dashboard
    path('logout',views.logout),
    path('send-message',views.sendMessage),
    path('view-messages',views.viewMessages),
    path('view-courses',views.viewCourses),
    path('update-password',views.updatePassword)
]
#role