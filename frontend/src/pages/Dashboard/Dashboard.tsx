import React from 'react';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const stats = [
    { label: 'Active Detections', value: '127', icon: '🔍', color: 'text-green' },
    { label: 'Monitoring Sessions', value: '23', icon: '📡', color: 'text-blue' },
    { label: 'Alerts Today', value: '15', icon: '⚠️', color: 'text-warning' },
    { label: 'System Health', value: '98%', icon: '💚', color: 'text-success' },
  ];

  const recentActivity = [
    { action: 'New detection detected', time: '2 minutes ago', type: 'detection' },
    { action: 'Monitoring session started', time: '5 minutes ago', type: 'monitoring' },
    { action: 'Alert threshold exceeded', time: '12 minutes ago', type: 'alert' },
    { action: 'User login detected', time: '15 minutes ago', type: 'user' },
    { action: 'System backup completed', time: '1 hour ago', type: 'system' },
  ];

  const quickActions = [
    { label: 'Start Detection', action: 'detection', icon: '🚀' },
    { label: 'Monitor Platform', action: 'monitoring', icon: '📡' },
    { label: 'Generate Report', action: 'analytics', icon: '📊' },
    { label: 'User Management', action: 'users', icon: '👥' },
  ];

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="glow-text">System Dashboard</h1>
        <p className="text-muted">Real-time monitoring and control center</p>
      </div>

      {/* Stats Grid */}
      <div className="row">
        {stats.map((stat, index) => (
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

      {/* Main Content Grid */}
      <div className="row">
        {/* Quick Actions */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Quick Actions</h3>
            </div>
            <div className="quick-actions">
              {quickActions.map((action, index) => (
                <button key={index} className="btn btn-primary quick-action-btn">
                  <span className="action-icon">{action.icon}</span>
                  {action.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* System Status */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">System Status</h3>
            </div>
            <div className="system-status">
              <div className="status-item">
                <span className="status-label">Database:</span>
                <span className="status-value text-success">ONLINE</span>
              </div>
              <div className="status-item">
                <span className="status-label">API Server:</span>
                <span className="status-value text-success">ONLINE</span>
              </div>
              <div className="status-item">
                <span className="status-label">ML Models:</span>
                <span className="status-value text-success">LOADED</span>
              </div>
              <div className="status-item">
                <span className="status-label">Security:</span>
                <span className="status-value text-success">ACTIVE</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Recent Activity</h3>
            </div>
            <div className="activity-list">
              {recentActivity.map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-icon">
                    {activity.type === 'detection' && '🔍'}
                    {activity.type === 'monitoring' && '📡'}
                    {activity.type === 'alert' && '⚠️'}
                    {activity.type === 'user' && '👤'}
                    {activity.type === 'system' && '⚙️'}
                  </div>
                  <div className="activity-content">
                    <div className="activity-action">{activity.action}</div>
                    <div className="activity-time">{activity.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Terminal Console */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">System Console</h3>
            </div>
            <div className="terminal console">
              <div className="console-line">{'>'} System initialized successfully</div>
              <div className="console-line">{'>'} Loading security protocols...</div>
              <div className="console-line">{'>'} Monitoring systems active</div>
              <div className="console-line">{'>'} Ready for commands</div>
              <div className="console-line">{'>'} _</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
