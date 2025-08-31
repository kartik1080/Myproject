from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    DrugCategory, DetectionPattern, Platform, DetectionResult,
    DetectionAnalytics, DetectionRule
)
from .serializers import (
    DrugCategorySerializer, DetectionPatternSerializer, PlatformSerializer,
    DetectionResultSerializer, DetectionResultCreateSerializer, DetectionResultUpdateSerializer,
    DetectionAnalyticsSerializer, DetectionRuleSerializer, DetectionStatsSerializer,
    BulkDetectionSerializer, DetectionSearchSerializer
)


class DrugCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrugCategory.objects.all()
    serializer_class = DrugCategorySerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def with_patterns(self, request):
        categories = self.get_queryset().prefetch_related('detectionpattern_set')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class DetectionPatternViewSet(viewsets.ModelViewSet):
    queryset = DetectionPattern.objects.all()
    serializer_class = DetectionPatternSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DetectionPattern.objects.all()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def test_pattern(self, request, pk=None):
        pattern = self.get_object()
        test_content = request.data.get('content', '')
        
        if not test_content:
            return Response({'error': 'Test content required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Simple pattern matching (can be enhanced with ML models)
        confidence = 0.0
        if pattern.keywords:
            keywords = pattern.keywords.lower().split(',')
            content_lower = test_content.lower()
            matches = sum(1 for keyword in keywords if keyword.strip() in content_lower)
            confidence = min(1.0, matches / len(keywords)) if keywords else 0.0
        
        return Response({
            'pattern': DetectionPatternSerializer(pattern).data,
            'test_content': test_content,
            'confidence_score': confidence,
            'matched': confidence > 0.5
        })


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        platform = self.get_object()
        
        try:
            # Test platform connection (placeholder for actual implementation)
            # This would typically involve testing API keys, connectivity, etc.
            return Response({
                'platform': PlatformSerializer(platform).data,
                'status': 'connected',
                'message': 'Platform connection test successful'
            })
        except Exception as e:
            return Response({
                'platform': PlatformSerializer(platform).data,
                'status': 'failed',
                'message': f'Connection test failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class DetectionResultViewSet(viewsets.ModelViewSet):
    queryset = DetectionResult.objects.all()
    serializer_class = DetectionResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DetectionResult.objects.select_related(
            'category', 'pattern', 'platform', 'assigned_to'
        ).all()
        
        # Filter by user role
        if self.request.user.role == 'USER':
            queryset = queryset.filter(assigned_to=self.request.user)
        elif self.request.user.role == 'MANAGER':
            queryset = queryset.filter(assigned_to__organization=self.request.user.organization)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DetectionResultCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DetectionResultUpdateSerializer
        return DetectionResultSerializer
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        detection = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from users.models import User
            user = User.objects.get(id=user_id)
            detection.assigned_to = user
            detection.status = 'ASSIGNED'
            detection.save()
            
            return Response({
                'message': 'Detection assigned successfully',
                'detection': DetectionResultSerializer(detection).data
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        detection = self.get_object()
        review_notes = request.data.get('review_notes', '')
        is_confirmed = request.data.get('is_confirmed', False)
        
        detection.review_notes = review_notes
        detection.status = 'CONFIRMED' if is_confirmed else 'REJECTED'
        detection.reviewed_at = timezone.now()
        detection.reviewed_by = request.user
        detection.save()
        
        return Response({
            'message': 'Detection reviewed successfully',
            'detection': DetectionResultSerializer(detection).data
        })
    
    @action(detail=True, methods=['post'])
    def escalate(self, request, pk=None):
        detection = self.get_object()
        escalation_level = request.data.get('escalation_level', 'MEDIUM')
        escalation_reason = request.data.get('escalation_reason', '')
        
        detection.escalation_level = escalation_level
        detection.escalation_reason = escalation_reason
        detection.status = 'ESCALATED'
        detection.escalated_at = timezone.now()
        detection.escalated_by = request.user
        detection.save()
        
        return Response({
            'message': 'Detection escalated successfully',
            'detection': DetectionResultSerializer(detection).data
        })
    
    @action(detail=True, methods=['post'])
    def mark_false_positive(self, request, pk=None):
        detection = self.get_object()
        reason = request.data.get('reason', '')
        
        detection.status = 'FALSE_POSITIVE'
        detection.false_positive_reason = reason
        detection.false_positive_at = timezone.now()
        detection.false_positive_by = request.user
        detection.save()
        
        return Response({
            'message': 'Detection marked as false positive',
            'detection': DetectionResultSerializer(detection).data
        })
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = BulkDetectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        platform_id = serializer.validated_data['platform_id']
        detections_data = serializer.validated_data['detections']
        
        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            return Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        created_detections = []
        for detection_data in detections_data:
            detection_data['platform'] = platform
            detection = DetectionResult.objects.create(**detection_data)
            created_detections.append(detection)
        
        return Response({
            'message': f'{len(created_detections)} detections created successfully',
            'detections': DetectionResultSerializer(created_detections, many=True).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        serializer = DetectionSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        queryset = self.get_queryset()
        data = serializer.validated_data
        
        if data.get('query'):
            queryset = queryset.filter(
                Q(content__icontains=data['query']) |
                Q(location__icontains=data['query'])
            )
        
        if data.get('category'):
            queryset = queryset.filter(category_id=data['category'])
        
        if data.get('platform'):
            queryset = queryset.filter(platform_id=data['platform'])
        
        if data.get('status'):
            queryset = queryset.filter(status=data['status'])
        
        if data.get('date_from'):
            queryset = queryset.filter(created_at__gte=data['date_from'])
        
        if data.get('date_to'):
            queryset = queryset.filter(created_at__lte=data['date_to'])
        
        if data.get('confidence_min'):
            queryset = queryset.filter(confidence_score__gte=data['confidence_min'])
        
        if data.get('confidence_max'):
            queryset = queryset.filter(confidence_score__lte=data['confidence_max'])
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = self.get_queryset()
        
        total_detections = queryset.count()
        pending_review = queryset.filter(status='PENDING').count()
        confirmed_detections = queryset.filter(status='CONFIRMED').count()
        false_positives = queryset.filter(status='FALSE_POSITIVE').count()
        
        detections_by_category = dict(
            queryset.values('category__name').annotate(count=Count('id'))
        )
        
        detections_by_platform = dict(
            queryset.values('platform__name').annotate(count=Count('id'))
        )
        
        average_confidence = queryset.aggregate(avg_confidence=Avg('confidence_score'))['avg_confidence'] or 0.0
        
        recent_detections = queryset.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        data = {
            'total_detections': total_detections,
            'pending_review': pending_review,
            'confirmed_detections': confirmed_detections,
            'false_positives': false_positives,
            'detections_by_category': detections_by_category,
            'detections_by_platform': detections_by_platform,
            'average_confidence': round(average_confidence, 2),
            'recent_detections': recent_detections
        }
        
        serializer = DetectionStatsSerializer(data)
        return Response(serializer.data)


class DetectionAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetectionAnalytics.objects.all()
    serializer_class = DetectionAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def daily_stats(self, request):
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        analytics = DetectionAnalytics.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        serializer = self.get_serializer(analytics, many=True)
        return Response(serializer.data)


class DetectionRuleViewSet(viewsets.ModelViewSet):
    queryset = DetectionRule.objects.all()
    serializer_class = DetectionRuleSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def test_rule(self, request, pk=None):
        rule = self.get_object()
        test_content = request.data.get('content', '')
        
        if not test_content:
            return Response({'error': 'Test content required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Test rule against content (placeholder for actual implementation)
        # This would typically involve applying the rule's logic
        matches = rule.test_content(test_content)
        
        return Response({
            'rule': DetectionRuleSerializer(rule).data,
            'test_content': test_content,
            'matches': matches
        })
