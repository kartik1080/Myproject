from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    AnalyticsReport, TrendAnalysis, GeographicAnalysis, 
    UserBehaviorAnalysis, PerformanceMetrics, AlertMetrics
)
from .serializers import (
    AnalyticsReportSerializer, TrendAnalysisSerializer, 
    GeographicAnalysisSerializer, UserBehaviorAnalysisSerializer,
    PerformanceMetricsSerializer, AlertMetricsSerializer
)


class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.all()
    serializer_class = AnalyticsReportSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        report = self.get_object()
        # Placeholder for download logic
        return Response({'message': 'Report download initiated'})
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        report = self.get_object()
        # Placeholder for regeneration logic
        return Response({'message': 'Report regeneration initiated'})


class TrendAnalysisViewSet(viewsets.ModelViewSet):
    queryset = TrendAnalysis.objects.all()
    serializer_class = TrendAnalysisSerializer
    permission_classes = [IsAuthenticated]


class GeographicAnalysisViewSet(viewsets.ModelViewSet):
    queryset = GeographicAnalysis.objects.all()
    serializer_class = GeographicAnalysisSerializer
    permission_classes = [IsAuthenticated]


class UserBehaviorAnalysisViewSet(viewsets.ModelViewSet):
    queryset = UserBehaviorAnalysis.objects.all()
    serializer_class = UserBehaviorAnalysisSerializer
    permission_classes = [IsAuthenticated]


class PerformanceMetricsViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetrics.objects.all()
    serializer_class = PerformanceMetricsSerializer
    permission_classes = [IsAuthenticated]


class AlertMetricsViewSet(viewsets.ModelViewSet):
    queryset = AlertMetrics.objects.all()
    serializer_class = AlertMetricsSerializer
    permission_classes = [IsAuthenticated]


# Custom API Views for specific endpoints
class AnalyticsDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Analytics dashboard endpoint'})


class AnalyticsOverviewView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Analytics overview endpoint'})


class TrendsDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Trends dashboard endpoint'})


class GeographicDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Geographic dashboard endpoint'})


class PerformanceDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Performance dashboard endpoint'})


class LiveAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Live analytics endpoint'})


class AnalyticsStreamView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Analytics stream endpoint'})


class LiveInsightsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Live insights endpoint'})


class ChartsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Charts endpoint'})


class TrendChartsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Trend charts endpoint'})


class GeographicChartsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Geographic charts endpoint'})


class PerformanceChartsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Performance charts endpoint'})


class AnalyticsExportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Analytics export endpoint'})


class ExportReportsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Export reports endpoint'})


class ExportChartsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Export charts endpoint'})


class ExportDataView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Export data endpoint'})


class BulkGenerateReportsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        report_types = request.data.get('report_types', [])
        return Response({'message': f'Generating {len(report_types)} reports'})


class BulkExportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        export_types = request.data.get('export_types', [])
        return Response({'message': f'Exporting {len(export_types)} items'})


class BulkDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        item_ids = request.data.get('item_ids', [])
        return Response({'message': f'Deleting {len(item_ids)} items'})


class AnalyticsSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Analytics search endpoint'})


class AnalyticsFilterView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Analytics filter endpoint'})


# Report generation views
class GenerateReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Report generation endpoint'})


class GenerateDailyReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Daily report generation endpoint'})


class GenerateWeeklyReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Weekly report generation endpoint'})


class GenerateMonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Monthly report generation endpoint'})


class GenerateCustomReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Custom report generation endpoint'})


class DownloadReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, report_id):
        return Response({'message': f'Downloading report {report_id}'})


class RegenerateReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, report_id):
        return Response({'message': f'Regenerating report {report_id}'})


# Legacy view names for backward compatibility
AnalyticsReportListView = AnalyticsReportViewSet.as_view({'get': 'list'})
AnalyticsReportDetailView = AnalyticsReportViewSet.as_view({'get': 'retrieve'})
AnalyticsReportCreateView = AnalyticsReportViewSet.as_view({'post': 'create'})
AnalyticsReportUpdateView = AnalyticsReportViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
AnalyticsReportDeleteView = AnalyticsReportViewSet.as_view({'delete': 'destroy'})

TrendAnalysisListView = TrendAnalysisViewSet.as_view({'get': 'list'})
TrendAnalysisDetailView = TrendAnalysisViewSet.as_view({'get': 'retrieve'})
TrendAnalysisCreateView = TrendAnalysisViewSet.as_view({'post': 'create'})
TrendAnalysisUpdateView = TrendAnalysisViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
TrendAnalysisDeleteView = TrendAnalysisViewSet.as_view({'delete': 'destroy'})

GeographicAnalysisListView = GeographicAnalysisViewSet.as_view({'get': 'list'})
GeographicAnalysisDetailView = GeographicAnalysisViewSet.as_view({'get': 'retrieve'})
GeographicAnalysisCreateView = GeographicAnalysisViewSet.as_view({'post': 'create'})
GeographicAnalysisUpdateView = GeographicAnalysisViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
GeographicAnalysisDeleteView = GeographicAnalysisViewSet.as_view({'delete': 'destroy'})

UserBehaviorAnalysisListView = UserBehaviorAnalysisViewSet.as_view({'get': 'list'})
UserBehaviorAnalysisDetailView = UserBehaviorAnalysisViewSet.as_view({'get': 'retrieve'})
UserBehaviorAnalysisCreateView = UserBehaviorAnalysisViewSet.as_view({'post': 'create'})
UserBehaviorAnalysisUpdateView = UserBehaviorAnalysisViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
UserBehaviorAnalysisDeleteView = UserBehaviorAnalysisViewSet.as_view({'delete': 'destroy'})

PerformanceMetricsListView = PerformanceMetricsViewSet.as_view({'get': 'list'})
PerformanceMetricsDetailView = PerformanceMetricsViewSet.as_view({'get': 'retrieve'})
PerformanceMetricsCreateView = PerformanceMetricsViewSet.as_view({'post': 'create'})
PerformanceMetricsUpdateView = PerformanceMetricsViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
PerformanceMetricsDeleteView = PerformanceMetricsViewSet.as_view({'delete': 'destroy'})

AlertMetricsListView = AlertMetricsViewSet.as_view({'get': 'list'})
AlertMetricsDetailView = AlertMetricsViewSet.as_view({'get': 'retrieve'})
AlertMetricsCreateView = AlertMetricsViewSet.as_view({'post': 'create'})
AlertMetricsUpdateView = AlertMetricsViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
AlertMetricsDeleteView = AlertMetricsViewSet.as_view({'delete': 'destroy'})
