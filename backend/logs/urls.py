from django.urls import path
from .views import LogFileApi, OperationApi, TraceBackApi

urlpatterns = [
    path('', LogFileApi.as_view()),
    path('operations/', OperationApi.as_view()),
    path('tracing/', TraceBackApi.as_view())
]