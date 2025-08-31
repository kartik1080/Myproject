import React from 'react';
import './Monitoring.css';

const Monitoring: React.FC = () => {
  const monitoringStats = [
    { label: 'Active Sessions', value: '23', icon: '📡', color: 'text-green' },
    { label: 'Platforms Monitored', value: '15', icon: '🌐', color: 'text-blue' },
    { label: 'Content Collected', value: '2.4K', icon: '📊', color: 'text-warning' },
    { label: 'System Uptime', value: '99.8%', icon: '💚', color: 'text-success' },
  ];

  const activeSessions = [
    { id: 1, platform: 'Telegram', status: 'Active', duration: '2h 15m', content: '1.2K messages' },
    { id: 2, platform: 'Instagram', status: 'Active', duration: '1h 45m', content: '856 posts' },
    { id: 3, platform: 'WhatsApp', status: 'Paused', duration: '45m', content: '234 chats' },
    { id: 4, platform: 'Facebook', status: 'Active', duration: '3h 20m', content: '1.8K posts' },
  ];

  const platformStatus = [
    { name: 'Telegram', status: 'online', latency: '45ms', lastCheck: '2 min ago' },
    { name: 'Instagram', status: 'online', latency: '67ms', lastCheck: '1 min ago' },
    { name: 'WhatsApp', status: 'online', latency: '89ms', lastCheck: '3 min ago' },
    { name: 'Facebook', status: 'online', latency: '123ms', lastCheck: '5 min ago' },
    { name: 'Twitter', status: 'offline', latency: 'N/A', lastCheck: '15 min ago' },
  ];

  return (
    <div className="monitoring-page">
      {/* Header */}
      <div className="page-header">
        <h1 className="glow-text">Platform Monitoring</h1>
        <p className="text-muted">Real-time monitoring and content collection system</p>
      </div>

      {/* Stats Grid */}
      <div className="row">
        {monitoringStats.map((stat, index) => (
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
        {/* Active Sessions */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Active Monitoring Sessions</h3>
            </div>
            <div className="session-list">
              {activeSessions.map((session) => (
                <div key={session.id} className="session-item">
                  <div className="session-icon">📡</div>
                  <div className="session-info">
                    <div className="session-platform">{session.platform}</div>
                    <div className="session-details">
                      <span className="session-duration">{session.duration}</span>
                      <span className="session-content">{session.content}</span>
                    </div>
                  </div>
                  <div className={`session-status status-${session.status.toLowerCase()}`}>
                    {session.status}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Platform Status */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Platform Status</h3>
            </div>
            <div className="platform-list">
              {platformStatus.map((platform, index) => (
                <div key={index} className="platform-item">
                  <div className="platform-icon">🌐</div>
                  <div className="platform-info">
                    <div className="platform-name">{platform.name}</div>
                    <div className="platform-meta">
                      <span className="platform-latency">Latency: {platform.latency}</span>
                      <span className="platform-check">Last: {platform.lastCheck}</span>
                    </div>
                  </div>
                  <div className={`platform-status status-${platform.status}`}>
                    {platform.status}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Monitoring Console */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Monitoring Console</h3>
            </div>
            <div className="terminal console">
              <div className="console-line">{'>'} Monitoring system initialized</div>
              <div className="console-line">{'>'} Connecting to platforms...</div>
              <div className="console-line">{'>'} Telegram: Connected (45ms latency)</div>
              <div className="console-line">{'>'} Instagram: Connected (67ms latency)</div>
              <div className="console-line">{'>'} WhatsApp: Connected (89ms latency)</div>
              <div className="console-line">{'>'} Facebook: Connected (123ms latency)</div>
              <div className="console-line">{'>'} All platforms online - monitoring active</div>
              <div className="console-line">{'>'} _</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Monitoring;
