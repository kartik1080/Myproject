"""
URL patterns for monitoring app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'monitoring'

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'sessions', views.MonitoringSessionViewSet, basename='session')
router.register(r'content', views.CollectedContentViewSet, basename='content')
router.register(r'rules', views.MonitoringRuleViewSet, basename='rule')
router.register(r'metrics', views.MonitoringMetricsViewSet, basename='metric')
router.register(r'connections', views.PlatformConnectionViewSet, basename='connection')

urlpatterns = [
    # Include ViewSet URLs
    path('', include(router.urls)),
    
    # Custom endpoints that use ViewSet actions
    path('sessions/<int:pk>/start/', views.MonitoringSessionViewSet.as_view({'post': 'start'}), name='start_session'),
    path('sessions/<int:pk>/pause/', views.MonitoringSessionViewSet.as_view({'post': 'pause'}), name='pause_session'),
    path('sessions/<int:pk>/stop/', views.MonitoringSessionViewSet.as_view({'post': 'stop'}), name='stop_session'),
    path('sessions/<int:pk>/restart/', views.MonitoringSessionViewSet.as_view({'post': 'restart'}), name='restart_session'),
    
    # Content management endpoints
    path('content/<int:pk>/mark-suspicious/', views.CollectedContentViewSet.as_view({'post': 'mark_suspicious'}), name='mark_suspicious'),
    path('content/<int:pk>/mark-clean/', views.CollectedContentViewSet.as_view({'post': 'mark_clean'}), name='mark_clean'),
    path('content/<int:pk>/process/', views.CollectedContentViewSet.as_view({'post': 'process'}), name='process_content'),
    
    # Rule execution endpoint
    path('rules/<int:pk>/execute/', views.MonitoringRuleViewSet.as_view({'post': 'execute'}), name='execute_rule'),
    
    # Metrics endpoints
    path('metrics/daily/', views.MonitoringMetricsViewSet.as_view({'get': 'daily_stats'}), name='daily_metrics'),
    
    # Connection management endpoints
    path('connections/<int:pk>/test/', views.PlatformConnectionViewSet.as_view({'post': 'test'}), name='test_connection'),
    path('connections/<int:pk>/reset-errors/', views.PlatformConnectionViewSet.as_view({'post': 'reset_errors'}), name='reset_errors'),
    
    # Dashboard and overview endpoints
    path('dashboard/', views.MonitoringDashboardView.as_view(), name='dashboard'),
    path('dashboard/overview/', views.MonitoringOverviewView.as_view(), name='overview'),
    path('dashboard/performance/', views.MonitoringPerformanceView.as_view(), name='performance'),
    path('dashboard/health/', views.MonitoringHealthView.as_view(), name='health'),
    
    # Real-time monitoring endpoints
    path('live/', views.LiveMonitoringView.as_view(), name='live_monitoring'),
    path('live/stream/', views.MonitoringStreamView.as_view(), name='monitoring_stream'),
    path('live/alerts/', views.LiveAlertsView.as_view(), name='live_alerts'),
    
    # Search and filtering endpoints
    path('search/', views.MonitoringSearchView.as_view(), name='search'),
    path('filter/', views.MonitoringFilterView.as_view(), name='filter'),
    
    # Export endpoints
    path('export/', views.MonitoringExportView.as_view(), name='export'),
    path('export/sessions/', views.ExportSessionsView.as_view(), name='export_sessions'),
    path('export/content/', views.ExportContentView.as_view(), name='export_content'),
    path('export/metrics/', views.ExportMetricsView.as_view(), name='export_metrics'),
    
    # Bulk operations
    path('bulk-start/', views.BulkStartSessionsView.as_view(), name='bulk_start'),
    path('bulk-stop/', views.BulkStopSessionsView.as_view(), name='bulk_stop'),
    path('bulk-pause/', views.BulkPauseSessionsView.as_view(), name='bulk_pause'),
    path('bulk-process-content/', views.BulkProcessContentView.as_view(), name='bulk_process_content'),
]
