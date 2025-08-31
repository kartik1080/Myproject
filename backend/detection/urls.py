"""
URL patterns for detection app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'detection'

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'categories', views.DrugCategoryViewSet, basename='category')
router.register(r'patterns', views.DetectionPatternViewSet, basename='pattern')
router.register(r'platforms', views.PlatformViewSet, basename='platform')
router.register(r'results', views.DetectionResultViewSet, basename='result')
router.register(r'analytics', views.DetectionAnalyticsViewSet, basename='analytics')
router.register(r'rules', views.DetectionRuleViewSet, basename='rule')

urlpatterns = [
    # Include ViewSet URLs
    path('', include(router.urls)),
    
    # Custom endpoints that use ViewSet actions
    path('results/<int:pk>/assign/', views.DetectionResultViewSet.as_view({'post': 'assign'}), name='assign_detection'),
    path('results/<int:pk>/review/', views.DetectionResultViewSet.as_view({'post': 'review'}), name='review_detection'),
    path('results/<int:pk>/escalate/', views.DetectionResultViewSet.as_view({'post': 'escalate'}), name='escalate_detection'),
    path('results/<int:pk>/mark-false-positive/', views.DetectionResultViewSet.as_view({'post': 'mark_false_positive'}), name='mark_false_positive'),
    
    # Pattern testing endpoint
    path('patterns/<int:pk>/test/', views.DetectionPatternViewSet.as_view({'post': 'test_pattern'}), name='test_pattern'),
    
    # Platform connection testing endpoint
    path('platforms/<int:pk>/test-connection/', views.PlatformViewSet.as_view({'post': 'test_connection'}), name='test_connection'),
    
    # Rule testing endpoint
    path('rules/<int:pk>/test/', views.DetectionRuleViewSet.as_view({'post': 'test_rule'}), name='test_rule'),
    
    # Analytics endpoints
    path('analytics/daily/', views.DetectionAnalyticsViewSet.as_view({'get': 'daily_stats'}), name='daily_analytics'),
    
    # Search and stats endpoints
    path('results/search/', views.DetectionResultViewSet.as_view({'get': 'search'}), name='search'),
    path('results/stats/', views.DetectionResultViewSet.as_view({'get': 'stats'}), name='stats'),
    
    # Bulk operations
    path('results/bulk-create/', views.DetectionResultViewSet.as_view({'post': 'bulk_create'}), name='bulk_create'),
]
