import React from 'react';
import './Detection.css';

const Detection: React.FC = () => {
  const detectionStats = [
    { label: 'Total Patterns', value: '1,247', icon: '🔍', color: 'text-green' },
    { label: 'Active Rules', value: '89', icon: '⚡', color: 'text-blue' },
    { label: 'Detections Today', value: '156', icon: '📊', color: 'text-warning' },
    { label: 'Accuracy Rate', value: '94.2%', icon: '🎯', color: 'text-success' },
  ];

  const recentDetections = [
    { id: 1, pattern: 'Cocaine Code Pattern', platform: 'Telegram', confidence: '98%', status: 'Confirmed' },
    { id: 2, pattern: 'Methamphetamine Slang', platform: 'Instagram', confidence: '87%', status: 'Pending' },
    { id: 3, pattern: 'Heroin Reference', platform: 'WhatsApp', confidence: '92%', status: 'Confirmed' },
    { id: 4, pattern: 'Cannabis Code', platform: 'Facebook', confidence: '76%', status: 'False Positive' },
  ];

  return (
    <div className="detection-page">
      {/* Header */}
      <div className="page-header">
        <h1 className="glow-text">Drug Detection Management</h1>
        <p className="text-muted">Advanced pattern recognition and detection system</p>
      </div>

      {/* Stats Grid */}
      <div className="row">
        {detectionStats.map((stat, index) => (
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
        {/* Detection Patterns */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Detection Patterns</h3>
            </div>
            <div className="pattern-list">
              <div className="pattern-item">
                <div className="pattern-icon">🔍</div>
                <div className="pattern-info">
                  <div className="pattern-name">Cocaine Code Pattern</div>
                  <div className="pattern-description">Detects coded references to cocaine</div>
                </div>
                <div className="pattern-status active">Active</div>
              </div>
              <div className="pattern-item">
                <div className="pattern-icon">⚡</div>
                <div className="pattern-info">
                  <div className="pattern-name">Methamphetamine Slang</div>
                  <div className="pattern-description">Identifies meth-related slang terms</div>
                </div>
                <div className="pattern-status active">Active</div>
              </div>
              <div className="pattern-item">
                <div className="pattern-icon">🎯</div>
                <div className="pattern-info">
                  <div className="pattern-name">Heroin References</div>
                  <div className="pattern-description">Detects heroin-related content</div>
                </div>
                <div className="pattern-status inactive">Inactive</div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Detections */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Recent Detections</h3>
            </div>
            <div className="detection-list">
              {recentDetections.map((detection) => (
                <div key={detection.id} className="detection-item">
                  <div className="detection-icon">🔍</div>
                  <div className="detection-info">
                    <div className="detection-pattern">{detection.pattern}</div>
                    <div className="detection-platform">{detection.platform}</div>
                  </div>
                  <div className="detection-meta">
                    <span className={`confidence ${detection.confidence.includes('9') ? 'high' : 'medium'}`}>
                      {detection.confidence}
                    </span>
                    <span className={`status status-${detection.status.toLowerCase().replace(' ', '-')}`}>
                      {detection.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Detection Console */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Detection Console</h3>
            </div>
            <div className="terminal console">
              <div className="console-line">{'>'} Detection system initialized</div>
              <div className="console-line">{'>'} Loading pattern database...</div>
              <div className="console-line">{'>'} Pattern matching engine active</div>
              <div className="console-line">{'>'} Monitoring 15 platforms</div>
              <div className="console-line">{'>'} Ready for real-time detection</div>
              <div className="console-line">{'>'} _</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Detection;
