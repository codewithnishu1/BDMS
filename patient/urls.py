from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', patient_signup),
    path('login/', patient_login),
    path('request_made/', blood_request),
    path('request_history/<str:eml>', request_history),
    path('patient_dashboard/<str:eml>', patient_dashBoard)
]
