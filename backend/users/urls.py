"""
URL patterns for users app.
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/refresh/', views.RefreshTokenView.as_view(), name='refresh_token'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # User sessions
    path('sessions/', views.UserSessionsView.as_view(), name='sessions'),
    path('sessions/<int:session_id>/end/', views.EndSessionView.as_view(), name='end_session'),
    
    # Admin endpoints (role-based access)
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
    path('admin/users/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:user_id>/activate/', views.ActivateUserView.as_view(), name='activate_user'),
    path('admin/users/<int:user_id>/deactivate/', views.DeactivateUserView.as_view(), name='deactivate_user'),
    path('admin/users/<int:user_id>/suspend/', views.SuspendUserView.as_view(), name='suspend_user'),
    path('admin/users/<int:user_id>/change-role/', views.ChangeUserRoleView.as_view(), name='change_user_role'),
    
    # User statistics and analytics
    path('admin/statistics/', views.UserStatisticsView.as_view(), name='user_statistics'),
    path('admin/activities/', views.UserActivitiesView.as_view(), name='user_activities'),
    
    # User search and filtering
    path('search/', views.UserSearchView.as_view(), name='user_search'),
    path('filter/', views.UserFilterView.as_view(), name='user_filter'),
    
    # Bulk operations
    path('admin/bulk-activate/', views.BulkActivateUsersView.as_view(), name='bulk_activate_users'),
    path('admin/bulk-deactivate/', views.BulkDeactivateUsersView.as_view(), name='bulk_deactivate_users'),
    path('admin/bulk-change-role/', views.BulkChangeUserRoleView.as_view(), name='bulk_change_user_role'),
]
