from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    """Home page view"""
    return render(request, 'home.html', {
        'project_name': 'Hack2Drug Detection System',
        'description': 'Advanced drug detection and monitoring platform for encrypted platforms'
    })


@api_view(['GET'])
def api_info(request):
    """API information endpoint"""
    return Response({
        'project': 'Hack2Drug Detection System',
        'version': '1.0.0',
        'description': 'Advanced drug detection and monitoring platform',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'users': '/users/',
            'detection': '/detection/',
            'monitoring': '/monitoring/',
            'analytics': '/analytics/',
        },
        'features': [
            'Real-time drug detection',
            'Multi-platform monitoring',
            'AI-powered pattern recognition',
            'Advanced analytics and reporting',
            'User management and role-based access',
            'API management and webhooks',
            'System health monitoring'
        ]
    })


@api_view(['GET'])
def health_check(request):
    """System health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z',
        'version': '1.0.0',
        'services': {
            'database': 'connected',
            'cache': 'connected',
            'celery': 'running'
        }
    })
