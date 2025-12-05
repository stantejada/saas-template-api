from django.urls import path
from .views import AuditLogViewSet

audit_log_list = AuditLogViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('audit-logs/', audit_log_list, name='audit-log-list'),
]