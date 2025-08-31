"""
URL patterns for API app.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # API access logs
    path('logs/', views.APIAccessLogListView.as_view(), name='log_list'),
    path('logs/<int:log_id>/', views.APIAccessLogDetailView.as_view(), name='log_detail'),
    path('logs/clear/', views.ClearAccessLogsView.as_view(), name='clear_logs'),
    
    # API keys management
    path('keys/', views.APIKeyListView.as_view(), name='key_list'),
    path('keys/<int:key_id>/', views.APIKeyDetailView.as_view(), name='key_detail'),
    path('keys/create/', views.APIKeyCreateView.as_view(), name='key_create'),
    path('keys/<int:key_id>/update/', views.APIKeyUpdateView.as_view(), name='key_update'),
    path('keys/<int:key_id>/delete/', views.APIKeyDeleteView.as_view(), name='key_delete'),
    path('keys/<int:key_id>/regenerate/', views.RegenerateAPIKeyView.as_view(), name='regenerate_key'),
    path('keys/<int:key_id>/activate/', views.ActivateAPIKeyView.as_view(), name='activate_key'),
    path('keys/<int:key_id>/deactivate/', views.DeactivateAPIKeyView.as_view(), name='deactivate_key'),
    
    # Webhook endpoints
    path('webhooks/', views.WebhookEndpointListView.as_view(), name='webhook_list'),
    path('webhooks/<int:webhook_id>/', views.WebhookEndpointDetailView.as_view(), name='webhook_detail'),
    path('webhooks/create/', views.WebhookEndpointCreateView.as_view(), name='webhook_create'),
    path('webhooks/<int:webhook_id>/update/', views.WebhookEndpointUpdateView.as_view(), name='webhook_update'),
    path('webhooks/<int:webhook_id>/delete/', views.WebhookEndpointDeleteView.as_view(), name='webhook_delete'),
    path('webhooks/<int:webhook_id>/test/', views.TestWebhookView.as_view(), name='test_webhook'),
    path('webhooks/<int:webhook_id>/reset-stats/', views.ResetWebhookStatsView.as_view(), name='reset_webhook_stats'),
    
    # Data exports
    path('exports/', views.DataExportListView.as_view(), name='export_list'),
    path('exports/<int:export_id>/', views.DataExportDetailView.as_view(), name='export_detail'),
    path('exports/create/', views.DataExportCreateView.as_view(), name='export_create'),
    path('exports/<int:export_id>/update/', views.DataExportUpdateView.as_view(), name='export_update'),
    path('exports/<int:export_id>/delete/', views.DataExportDeleteView.as_view(), name='export_delete'),
    path('exports/<int:export_id>/download/', views.DownloadExportView.as_view(), name='download_export'),
    path('exports/<int:export_id>/retry/', views.RetryExportView.as_view(), name='retry_export'),
    path('exports/<int:export_id>/cancel/', views.CancelExportView.as_view(), name='cancel_export'),
    
    # System health
    path('health/', views.SystemHealthListView.as_view(), name='health_list'),
    path('health/<int:health_id>/', views.SystemHealthDetailView.as_view(), name='health_detail'),
    path('health/create/', views.SystemHealthCreateView.as_view(), name='health_create'),
    path('health/<int:health_id>/update/', views.SystemHealthUpdateView.as_view(), name='health_update'),
    path('health/<int:health_id>/delete/', views.SystemHealthDeleteView.as_view(), name='health_delete'),
    path('health/check/', views.CheckSystemHealthView.as_view(), name='check_health'),
    path('health/reset/', views.ResetSystemHealthView.as_view(), name='reset_health'),
    
    # API documentation
    path('docs/', views.APIDocumentationView.as_view(), name='documentation'),
    path('docs/endpoints/', views.APIEndpointsView.as_view(), name='endpoints'),
    path('docs/authentication/', views.APIAuthenticationView.as_view(), name='authentication'),
    path('docs/examples/', views.APIExamplesView.as_view(), name='examples'),
    
    # API testing
    path('test/', views.APITestView.as_view(), name='test'),
    path('test/endpoint/', views.TestEndpointView.as_view(), name='test_endpoint'),
    path('test/authentication/', views.TestAuthenticationView.as_view(), name='test_auth'),
    path('test/rate-limits/', views.TestRateLimitsView.as_view(), name='test_rate_limits'),
    
    # API statistics
    path('stats/', views.APIStatsView.as_view(), name='stats'),
    path('stats/usage/', views.APIUsageStatsView.as_view(), name='usage_stats'),
    path('stats/performance/', views.APIPerformanceStatsView.as_view(), name='performance_stats'),
    path('stats/errors/', views.APIErrorStatsView.as_view(), name='error_stats'),
    
    # Rate limiting
    path('rate-limits/', views.RateLimitListView.as_view(), name='rate_limit_list'),
    path('rate-limits/<int:limit_id>/', views.RateLimitDetailView.as_view(), name='rate_limit_detail'),
    path('rate-limits/create/', views.RateLimitCreateView.as_view(), name='rate_limit_create'),
    path('rate-limits/<int:limit_id>/update/', views.RateLimitUpdateView.as_view(), name='rate_limit_update'),
    path('rate-limits/<int:limit_id>/delete/', views.RateLimitDeleteView.as_view(), name='rate_limit_delete'),
    
    # API monitoring
    path('monitor/', views.APIMonitorView.as_view(), name='monitor'),
    path('monitor/endpoints/', views.EndpointMonitorView.as_view(), name='endpoint_monitor'),
    path('monitor/performance/', views.PerformanceMonitorView.as_view(), name='performance_monitor'),
    path('monitor/alerts/', views.APIAlertsView.as_view(), name='api_alerts'),
    
    # Bulk operations
    path('bulk-regenerate-keys/', views.BulkRegenerateKeysView.as_view(), name='bulk_regenerate_keys'),
    path('bulk-activate-keys/', views.BulkActivateKeysView.as_view(), name='bulk_activate_keys'),
    path('bulk-deactivate-keys/', views.BulkDeactivateKeysView.as_view(), name='bulk_deactivate_keys'),
    path('bulk-test-webhooks/', views.BulkTestWebhooksView.as_view(), name='bulk_test_webhooks'),
    path('bulk-check-health/', views.BulkCheckHealthView.as_view(), name='bulk_check_health'),
    
    # Search and filtering
    path('search/', views.APISearchView.as_view(), name='search'),
    path('filter/', views.APIFilterView.as_view(), name='filter'),
]
