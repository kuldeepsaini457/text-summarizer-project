
from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_summary,name="GetSummary"),
    path('abstractive',views.get_abstractive_summary,name="GetAbstractiveSummary"),
]