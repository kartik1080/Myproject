from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import User, UserProfile, UserSession, UserActivity
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    LoginSerializer, PasswordChangeSerializer, UserStatsSerializer,
    UserProfileSerializer, UserSessionSerializer, UserActivitySerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Create user session
        session = UserSession.objects.create(
            user=user,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            device_info=request.META.get('HTTP_USER_AGENT', ''),
            is_active=True
        )
        
        # Log activity
        UserActivity.objects.create(
            user=user,
            action='login',
            details=f'User logged in from {request.META.get("REMOTE_ADDR", "unknown")}',
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'session_id': session.id
        })


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # End active sessions
        UserSession.objects.filter(user=request.user, is_active=True).update(
            is_active=False,
            last_activity=timezone.now()
        )
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action='logout',
            details='User logged out',
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        logout(request)
        return Response({'message': 'Logout successful'})


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        return Response({'message': 'Token refresh endpoint'})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user.userprofile)
        return Response(serializer.data)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user.userprofile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        UserActivity.objects.create(
            user=user,
            action='password_change',
            details='Password changed successfully',
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'message': 'Password changed successfully'})


class UserSessionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        sessions = UserSession.objects.filter(user=request.user)
        serializer = UserSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class EndSessionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, session_id):
        try:
            session = UserSession.objects.get(id=session_id, user=request.user)
            session.is_active = False
            session.last_activity = timezone.now()
            session.save()
            return Response({'message': 'Session ended successfully'})
        except UserSession.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


class UserListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ActivateUserView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.status = User.ACTIVE
            user.save()
            return Response({'message': 'User activated successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class DeactivateUserView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.status = User.INACTIVE
            user.save()
            return Response({'message': 'User deactivated successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class SuspendUserView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.status = User.SUSPENDED
            user.save()
            return Response({'message': 'User suspended successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ChangeUserRoleView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            new_role = request.data.get('role')
            
            if new_role not in dict(User.ROLE_CHOICES):
                return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.role = new_role
            user.save()
            return Response({'message': 'User role changed successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserStatisticsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(status=User.ACTIVE).count()
        suspended_users = User.objects.filter(status=User.SUSPENDED).count()
        
        users_by_role = dict(User.objects.values_list('role').annotate(count=Count('id')))
        
        recent_registrations = User.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        active_sessions = UserSession.objects.filter(is_active=True).count()
        
        data = {
            'total_users': total_users,
            'active_users': active_users,
            'suspended_users': suspended_users,
            'users_by_role': users_by_role,
            'recent_registrations': recent_registrations,
            'active_sessions': active_sessions
        }
        
        return Response(data)


class UserActivitiesView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        activities = UserActivity.objects.all().order_by('-timestamp')[:100]
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Search query required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.role == User.ADMIN:
            users = User.objects.all()
        elif request.user.role == User.MANAGER:
            users = User.objects.filter(organization=request.user.organization)
        else:
            users = User.objects.filter(id=request.user.id)
        
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(organization__icontains=query)
        )
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserFilterView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        role = request.query_params.get('role')
        status_filter = request.query_params.get('status')
        organization = request.query_params.get('organization')
        
        if request.user.role == User.ADMIN:
            users = User.objects.all()
        elif request.user.role == User.MANAGER:
            users = User.objects.filter(organization=request.user.organization)
        else:
            users = User.objects.filter(id=request.user.id)
        
        if role:
            users = users.filter(role=role)
        if status_filter:
            users = users.filter(status=status_filter)
        if organization:
            users = users.filter(organization__icontains=organization)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class BulkActivateUsersView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        user_ids = request.data.get('user_ids', [])
        User.objects.filter(id__in=user_ids).update(status=User.ACTIVE)
        return Response({'message': f'{len(user_ids)} users activated successfully'})


class BulkDeactivateUsersView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        user_ids = request.data.get('user_ids', [])
        User.objects.filter(id__in=user_ids).update(status=User.INACTIVE)
        return Response({'message': f'{len(user_ids)} users deactivated successfully'})


class BulkChangeUserRoleView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        user_ids = request.data.get('user_ids', [])
        new_role = request.data.get('role')
        
        if new_role not in dict(User.ROLE_CHOICES):
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        User.objects.filter(id__in=user_ids).update(role=new_role)
        return Response({'message': f'{len(user_ids)} users role changed successfully'})
