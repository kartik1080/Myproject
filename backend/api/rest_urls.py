"""
Main REST API URL patterns for Hack2Drug system.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()

# User management
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'sessions', views.UserSessionViewSet, basename='session')
router.register(r'activities', views.UserActivityViewSet, basename='activity')

# Detection system
router.register(r'detection-results', views.DetectionResultViewSet, basename='detection-result')
router.register(r'detection-patterns', views.DetectionPatternViewSet, basename='detection-pattern')
router.register(r'drug-categories', views.DrugCategoryViewSet, basename='drug-category')
router.register(r'platforms', views.PlatformViewSet, basename='platform')
router.register(r'detection-rules', views.DetectionRuleViewSet, basename='detection-rule')
router.register(r'detection-analytics', views.DetectionAnalyticsViewSet, basename='detection-analytics')

# Monitoring system
router.register(r'monitoring-sessions', views.MonitoringSessionViewSet, basename='monitoring-session')
router.register(r'collected-content', views.CollectedContentViewSet, basename='collected-content')
router.register(r'monitoring-rules', views.MonitoringRuleViewSet, basename='monitoring-rule')
router.register(r'monitoring-metrics', views.MonitoringMetricsViewSet, basename='monitoring-metrics')
router.register(r'platform-connections', views.PlatformConnectionViewSet, basename='platform-connection')

# Analytics system
router.register(r'analytics-reports', views.AnalyticsReportViewSet, basename='analytics-report')
router.register(r'trend-analysis', views.TrendAnalysisViewSet, basename='trend-analysis')
router.register(r'geographic-analysis', views.GeographicAnalysisViewSet, basename='geographic-analysis')
router.register(r'user-behavior-analysis', views.UserBehaviorAnalysisViewSet, basename='user-behavior-analysis')
router.register(r'performance-metrics', views.PerformanceMetricsViewSet, basename='performance-metrics')
router.register(r'alert-metrics', views.AlertMetricsViewSet, basename='alert-metrics')

# API management
router.register(r'api-logs', views.APIAccessLogViewSet, basename='api-log')
router.register(r'api-keys', views.APIKeyViewSet, basename='api-key')
router.register(r'webhook-endpoints', views.WebhookEndpointViewSet, basename='webhook-endpoint')
router.register(r'data-exports', views.DataExportViewSet, basename='data-export')
router.register(r'system-health', views.SystemHealthViewSet, basename='system-health')

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    
    # Custom API endpoints
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('dashboard/recent-detections/', views.RecentDetectionsView.as_view(), name='recent-detections'),
    path('dashboard/platform-status/', views.PlatformStatusView.as_view(), name='platform-status'),
    
    # Detection actions
    path('detection-results/<int:pk>/assign/', views.AssignDetectionView.as_view(), name='assign-detection'),
    path('detection-results/<int:pk>/review/', views.ReviewDetectionView.as_view(), name='review-detection'),
    path('detection-results/<int:pk>/escalate/', views.EscalateDetectionView.as_view(), name='escalate-detection'),
    path('detection-results/<int:pk>/mark-false-positive/', views.MarkFalsePositiveView.as_view(), name='mark-false-positive'),
    path('detection-results/<int:pk>/add-notes/', views.AddDetectionNotesView.as_view(), name='add-detection-notes'),
    
    # Monitoring actions
    path('monitoring-sessions/<int:pk>/start/', views.StartMonitoringView.as_view(), name='start-monitoring'),
    path('monitoring-sessions/<int:pk>/stop/', views.StopMonitoringView.as_view(), name='stop-monitoring'),
    path('monitoring-sessions/<int:pk>/test-connection/', views.TestMonitoringConnectionView.as_view(), name='test-monitoring-connection'),
    
    # Analytics endpoints
    path('analytics/trends/', views.TrendsAnalyticsView.as_view(), name='trends-analytics'),
    path('analytics/geographic/', views.GeographicAnalyticsView.as_view(), name='geographic-analytics'),
    path('analytics/performance/', views.PerformanceAnalyticsView.as_view(), name='performance-analytics'),
    path('analytics/export/', views.AnalyticsExportView.as_view(), name='analytics-export'),
    
    # Real-time endpoints
    path('realtime/detections/', views.RealtimeDetectionsView.as_view(), name='realtime-detections'),
    path('realtime/monitoring/', views.RealtimeMonitoringView.as_view(), name='realtime-monitoring'),
    path('realtime/alerts/', views.RealtimeAlertsView.as_view(), name='realtime-alerts'),
    
    # Search and filtering
    path('search/', views.GlobalSearchView.as_view(), name='global-search'),
    path('search/detections/', views.SearchDetectionsView.as_view(), name='search-detections'),
    path('search/users/', views.SearchUsersView.as_view(), name='search-users'),
    path('search/content/', views.SearchContentView.as_view(), name='search-content'),
    
    # Bulk operations
    path('bulk/detections/', views.BulkDetectionOperationsView.as_view(), name='bulk-detections'),
    path('bulk/users/', views.BulkUserOperationsView.as_view(), name='bulk-users'),
    path('bulk/monitoring/', views.BulkMonitoringOperationsView.as_view(), name='bulk-monitoring'),
    
    # Authentication endpoints
    path('auth/', include('users.urls')),
    
    # Include app-specific API URLs
    path('detection/', include('detection.urls')),
    path('monitoring/', include('monitoring.urls')),
    path('analytics/', include('analytics.urls')),
]
