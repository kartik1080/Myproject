"""
URL patterns for analytics app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'analytics'

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'reports', views.AnalyticsReportViewSet, basename='report')
router.register(r'trends', views.TrendAnalysisViewSet, basename='trend')
router.register(r'geographic', views.GeographicAnalysisViewSet, basename='geographic')
router.register(r'behavior', views.UserBehaviorAnalysisViewSet, basename='behavior')
router.register(r'performance', views.PerformanceMetricsViewSet, basename='performance')
router.register(r'alerts', views.AlertMetricsViewSet, basename='alert')

urlpatterns = [
    # Include ViewSet URLs
    path('', include(router.urls)),
    
    # Custom endpoints that use ViewSet actions
    path('reports/<int:pk>/download/', views.AnalyticsReportViewSet.as_view({'post': 'download'}), name='download_report'),
    path('reports/<int:pk>/regenerate/', views.AnalyticsReportViewSet.as_view({'post': 'regenerate'}), name='regenerate_report'),
    
    # Report generation endpoints
    path('generate/', views.GenerateReportView.as_view(), name='generate_report'),
    path('generate/daily/', views.GenerateDailyReportView.as_view(), name='generate_daily'),
    path('generate/weekly/', views.GenerateWeeklyReportView.as_view(), name='generate_weekly'),
    path('generate/monthly/', views.GenerateMonthlyReportView.as_view(), name='generate_monthly'),
    path('generate/custom/', views.GenerateCustomReportView.as_view(), name='generate_custom'),
    
    # Analytics dashboard endpoints
    path('dashboard/', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('dashboard/overview/', views.AnalyticsOverviewView.as_view(), name='overview'),
    path('dashboard/trends/', views.TrendsDashboardView.as_view(), name='trends_dashboard'),
    path('dashboard/geographic/', views.GeographicDashboardView.as_view(), name='geographic_dashboard'),
    path('dashboard/performance/', views.PerformanceDashboardView.as_view(), name='performance_dashboard'),
    
    # Real-time analytics endpoints
    path('live/', views.LiveAnalyticsView.as_view(), name='live_analytics'),
    path('live/stream/', views.AnalyticsStreamView.as_view(), name='analytics_stream'),
    path('live/insights/', views.LiveInsightsView.as_view(), name='live_insights'),
    
    # Data visualization endpoints
    path('charts/', views.ChartsView.as_view(), name='charts'),
    path('charts/trends/', views.TrendChartsView.as_view(), name='trend_charts'),
    path('charts/geographic/', views.GeographicChartsView.as_view(), name='geographic_charts'),
    path('charts/performance/', views.PerformanceChartsView.as_view(), name='performance_charts'),
    
    # Export and sharing endpoints
    path('export/', views.AnalyticsExportView.as_view(), name='export'),
    path('export/reports/', views.ExportReportsView.as_view(), name='export_reports'),
    path('export/charts/', views.ExportChartsView.as_view(), name='export_charts'),
    path('export/data/', views.ExportDataView.as_view(), name='export_data'),
    
    # Bulk operations
    path('bulk-generate/', views.BulkGenerateReportsView.as_view(), name='bulk_generate'),
    path('bulk-export/', views.BulkExportView.as_view(), name='bulk_export'),
    path('bulk-delete/', views.BulkDeleteView.as_view(), name='bulk_delete'),
    
    # Search and filtering
    path('search/', views.AnalyticsSearchView.as_view(), name='search'),
    path('filter/', views.AnalyticsFilterView.as_view(), name='filter'),
]
