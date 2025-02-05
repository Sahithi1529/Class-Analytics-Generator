from django.urls import path
from . import views
urlpatterns = [
    path('',views.facultyLogin),
    path("faculty-dashboard",views.facultyDashboard),
    path('logout',views.logout),
    path('send-message',views.sendMessage),
    path('view-messages',views.viewMessages),
    path('view-courses',views.viewCourses)
]