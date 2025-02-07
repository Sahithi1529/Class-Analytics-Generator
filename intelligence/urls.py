from django.urls import path
from . import views
urlpatterns = [
    path('test',views.Test),
    path('start-tracking',views.startTracking),
    path('generate-analytics',views.generateAnalytics),
    path('show-analytics',views.showAnalytics,name="show-analytics")
   
]