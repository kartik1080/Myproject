import React from 'react';
import './Users.css';

const Users: React.FC = () => {
  const userStats = [
    { label: 'Total Users', value: '156', icon: '👥', color: 'text-green' },
    { label: 'Active Users', value: '89', icon: '🟢', color: 'text-blue' },
    { label: 'Admin Users', value: '12', icon: '👑', color: 'text-warning' },
    { label: 'New Today', value: '5', icon: '🆕', color: 'text-success' },
  ];

  const recentUsers = [
    { id: 1, name: 'John Smith', role: 'Analyst', status: 'Active', lastLogin: '2 hours ago' },
    { id: 2, name: 'Sarah Johnson', role: 'Admin', status: 'Active', lastLogin: '1 hour ago' },
    { id: 3, name: 'Mike Davis', role: 'Viewer', status: 'Inactive', lastLogin: '3 days ago' },
    { id: 4, name: 'Lisa Wilson', role: 'Analyst', status: 'Active', lastLogin: '30 min ago' },
  ];

  const userRoles = [
    { role: 'Super Admin', permissions: 'Full access', users: 2, color: 'danger' },
    { role: 'Admin', permissions: 'User management', users: 10, color: 'warning' },
    { role: 'Analyst', permissions: 'Data analysis', users: 45, color: 'success' },
    { role: 'Viewer', permissions: 'Read-only access', users: 99, color: 'info' },
  ];

  return (
    <div className="users-page">
      {/* Header */}
      <div className="page-header">
        <h1 className="glow-text">User Management</h1>
        <p className="text-muted">Comprehensive user administration and role management</p>
      </div>

      {/* Stats Grid */}
      <div className="row">
        {userStats.map((stat, index) => (
          <div key={index} className="col-3">
            <div className="card stat-card">
              <div className="stat-content">
                <div className="stat-icon">{stat.icon}</div>
                <div className="stat-info">
                  <div className={`stat-value ${stat.color}`}>{stat.value}</div>
                  <div className="stat-label">{stat.label}</div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Main Content */}
      <div className="row">
        {/* Recent Users */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Recent Users</h3>
            </div>
            <div className="user-list">
              {recentUsers.map((user) => (
                <div key={user.id} className="user-item">
                  <div className="user-avatar">
                    {user.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div className="user-info">
                    <div className="user-name">{user.name}</div>
                    <div className="user-meta">
                      <span className="user-role">{user.role}</span>
                      <span className="user-login">Last: {user.lastLogin}</span>
                    </div>
                  </div>
                  <div className={`user-status status-${user.status.toLowerCase()}`}>
                    {user.status}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* User Roles */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">User Roles & Permissions</h3>
            </div>
            <div className="role-list">
              {userRoles.map((role, index) => (
                <div key={index} className="role-item">
                  <div className="role-icon">👤</div>
                  <div className="role-info">
                    <div className="role-name">{role.role}</div>
                    <div className="role-meta">
                      <span className="role-permissions">{role.permissions}</span>
                      <span className="role-users">{role.users} users</span>
                    </div>
                  </div>
                  <div className={`role-badge role-${role.color}`}>
                    {role.users}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* User Management Console */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">User Management Console</h3>
            </div>
            <div className="terminal console">
              <div className="console-line">{'>'} User management system initialized</div>
              <div className="console-line">{'>'} Loading user database...</div>
              <div className="console-line">{'>'} Connected to authentication service</div>
              <div className="console-line">{'>'} Role permissions loaded</div>
              <div className="console-line">{'>'} User session monitoring active</div>
              <div className="console-line">{'>'} Ready for user operations</div>
              <div className="console-line">{'>'} _</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Users;
