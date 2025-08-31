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
    MonitoringSession, CollectedContent, MonitoringRule, 
    MonitoringMetrics, PlatformConnection
)
from .serializers import (
    MonitoringSessionSerializer, CollectedContentSerializer, 
    MonitoringRuleSerializer, MonitoringMetricsSerializer, 
    PlatformConnectionSerializer
)


class MonitoringSessionViewSet(viewsets.ModelViewSet):
    queryset = MonitoringSession.objects.all()
    serializer_class = MonitoringSessionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        session = self.get_object()
        session.status = 'ACTIVE'
        session.started_at = timezone.now()
        session.save()
        return Response({'message': 'Monitoring session started'})
    
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        session = self.get_object()
        session.status = 'STOPPED'
        session.stopped_at = timezone.now()
        session.save()
        return Response({'message': 'Monitoring session stopped'})
    
    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        session = self.get_object()
        session.status = 'PAUSED'
        session.paused_at = timezone.now()
        session.save()
        return Response({'message': 'Monitoring session paused'})
    
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        session = self.get_object()
        session.status = 'ACTIVE'
        session.restarted_at = timezone.now()
        session.save()
        return Response({'message': 'Monitoring session restarted'})


class CollectedContentViewSet(viewsets.ModelViewSet):
    queryset = CollectedContent.objects.all()
    serializer_class = CollectedContentSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def mark_suspicious(self, request, pk=None):
        content = self.get_object()
        content.status = 'SUSPICIOUS'
        content.save()
        return Response({'message': 'Content marked as suspicious'})
    
    @action(detail=True, methods=['post'])
    def mark_clean(self, request, pk=None):
        content = self.get_object()
        content.status = 'CLEAN'
        content.save()
        return Response({'message': 'Content marked as clean'})
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        content = self.get_object()
        content.status = 'PROCESSED'
        content.processed_at = timezone.now()
        content.save()
        return Response({'message': 'Content processed'})


class MonitoringRuleViewSet(viewsets.ModelViewSet):
    queryset = MonitoringRule.objects.all()
    serializer_class = MonitoringRuleSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        rule = self.get_object()
        # Placeholder for rule execution logic
        return Response({'message': 'Rule executed'})


class MonitoringMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MonitoringMetrics.objects.all()
    serializer_class = MonitoringMetricsSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def daily_stats(self, request):
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        metrics = MonitoringMetrics.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)


class PlatformConnectionViewSet(viewsets.ModelViewSet):
    queryset = PlatformConnection.objects.all()
    serializer_class = PlatformConnectionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        connection = self.get_object()
        # Placeholder for connection testing logic
        return Response({'message': 'Connection tested'})
    
    @action(detail=True, methods=['post'])
    def reset_errors(self, request, pk=None):
        connection = self.get_object()
        connection.error_count = 0
        connection.last_error = None
        connection.save()
        return Response({'message': 'Connection errors reset'})


# Custom API Views for specific endpoints
class MonitoringDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring dashboard endpoint'})


class MonitoringOverviewView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring overview endpoint'})


class MonitoringPerformanceView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring performance endpoint'})


class MonitoringHealthView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring health endpoint'})


class LiveMonitoringView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Live monitoring endpoint'})


class MonitoringStreamView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring stream endpoint'})


class LiveAlertsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Live alerts endpoint'})


class MonitoringSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring search endpoint'})


class MonitoringFilterView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring filter endpoint'})


class MonitoringExportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Monitoring export endpoint'})


class ExportSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Export sessions endpoint'})


class ExportContentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Export content endpoint'})


class ExportMetricsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Export metrics endpoint'})


class BulkStartSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        session_ids = request.data.get('session_ids', [])
        MonitoringSession.objects.filter(id__in=session_ids).update(
            status='ACTIVE', started_at=timezone.now()
        )
        return Response({'message': f'{len(session_ids)} sessions started'})


class BulkStopSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        session_ids = request.data.get('session_ids', [])
        MonitoringSession.objects.filter(id__in=session_ids).update(
            status='STOPPED', stopped_at=timezone.now()
        )
        return Response({'message': f'{len(session_ids)} sessions stopped'})


class BulkPauseSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        session_ids = request.data.get('session_ids', [])
        MonitoringSession.objects.filter(id__in=session_ids).update(
            status='PAUSED', paused_at=timezone.now()
        )
        return Response({'message': f'{len(session_ids)} sessions paused'})


class BulkProcessContentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        content_ids = request.data.get('content_ids', [])
        CollectedContent.objects.filter(id__in=content_ids).update(
            status='PROCESSED', processed_at=timezone.now()
        )
        return Response({'message': f'{len(content_ids)} content items processed'})


# Legacy view names for backward compatibility
MonitoringSessionListView = MonitoringSessionViewSet.as_view({'get': 'list'})
MonitoringSessionDetailView = MonitoringSessionViewSet.as_view({'get': 'retrieve'})
MonitoringSessionCreateView = MonitoringSessionViewSet.as_view({'post': 'create'})
MonitoringSessionUpdateView = MonitoringSessionViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
MonitoringSessionDeleteView = MonitoringSessionViewSet.as_view({'delete': 'destroy'})

StartMonitoringSessionView = MonitoringSessionViewSet.as_view({'post': 'start'})
PauseMonitoringSessionView = MonitoringSessionViewSet.as_view({'post': 'pause'})
StopMonitoringSessionView = MonitoringSessionViewSet.as_view({'post': 'stop'})
RestartMonitoringSessionView = MonitoringSessionViewSet.as_view({'post': 'restart'})

CollectedContentView = CollectedContentViewSet.as_view({'get': 'list'})
CollectedContentDetailView = CollectedContentViewSet.as_view({'get': 'retrieve'})
MarkContentSuspiciousView = CollectedContentViewSet.as_view({'post': 'mark_suspicious'})
MarkContentCleanView = CollectedContentViewSet.as_view({'post': 'mark_clean'})
ProcessContentView = CollectedContentViewSet.as_view({'post': 'process'})

MonitoringRuleListView = MonitoringRuleViewSet.as_view({'get': 'list'})
MonitoringRuleDetailView = MonitoringRuleViewSet.as_view({'get': 'retrieve'})
MonitoringRuleCreateView = MonitoringRuleViewSet.as_view({'post': 'create'})
MonitoringRuleUpdateView = MonitoringRuleViewSet.as_view({'put': 'update', 'patch': 'partial_update'})
MonitoringRuleDeleteView = MonitoringRuleViewSet.as_view({'delete': 'destroy'})
ExecuteMonitoringRuleView = MonitoringRuleViewSet.as_view({'post': 'execute'})

MonitoringMetricsView = MonitoringMetricsViewSet.as_view({'get': 'list'})
DailyMetricsView = MonitoringMetricsViewSet.as_view({'get': 'daily_stats'})
WeeklyMetricsView = MonitoringMetricsViewSet.as_view({'get': 'list'})
MonthlyMetricsView = MonitoringMetricsViewSet.as_view({'get': 'list'})

PlatformConnectionListView = PlatformConnectionViewSet.as_view({'get': 'list'})
PlatformConnectionDetailView = PlatformConnectionViewSet.as_view({'get': 'retrieve'})
TestConnectionView = PlatformConnectionViewSet.as_view({'post': 'test'})
ResetConnectionErrorsView = PlatformConnectionViewSet.as_view({'post': 'reset_errors'})
