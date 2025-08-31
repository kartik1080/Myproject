import React from 'react';
import './Analytics.css';

const Analytics: React.FC = () => {
  const analyticsStats = [
    { label: 'Reports Generated', value: '156', icon: '📊', color: 'text-green' },
    { label: 'Data Points', value: '2.4M', icon: '📈', color: 'text-blue' },
    { label: 'Trends Identified', value: '89', icon: '📉', color: 'text-warning' },
    { label: 'Accuracy Score', value: '96.8%', icon: '🎯', color: 'text-success' },
  ];

  const recentReports = [
    { id: 1, title: 'Weekly Drug Trend Analysis', type: 'Weekly', status: 'Completed', size: '2.4MB' },
    { id: 2, title: 'Monthly Platform Report', type: 'Monthly', status: 'Processing', size: '5.1MB' },
    { id: 3, title: 'Geographic Distribution', type: 'Custom', status: 'Completed', size: '1.8MB' },
    { id: 4, title: 'User Behavior Analysis', type: 'Daily', status: 'Failed', size: 'N/A' },
  ];

  const dataTrends = [
    { name: 'Cocaine References', trend: 'up', change: '+12.5%', period: 'vs last week' },
    { name: 'Methamphetamine', trend: 'down', change: '-8.3%', period: 'vs last week' },
    { name: 'Heroin Mentions', trend: 'up', change: '+5.7%', period: 'vs last week' },
    { name: 'Cannabis Content', trend: 'stable', change: '0.2%', period: 'vs last week' },
  ];

  return (
    <div className="analytics-page">
      {/* Header */}
      <div className="page-header">
        <h1 className="glow-text">Analytics & Reporting</h1>
        <p className="text-muted">Comprehensive data analysis and insights dashboard</p>
      </div>

      {/* Stats Grid */}
      <div className="row">
        {analyticsStats.map((stat, index) => (
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
        {/* Recent Reports */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Recent Reports</h3>
            </div>
            <div className="report-list">
              {recentReports.map((report) => (
                <div key={report.id} className="report-item">
                  <div className="report-icon">📊</div>
                  <div className="report-info">
                    <div className="report-title">{report.title}</div>
                    <div className="report-meta">
                      <span className="report-type">{report.type}</span>
                      <span className="report-size">{report.size}</span>
                    </div>
                  </div>
                  <div className={`report-status status-${report.status.toLowerCase()}`}>
                    {report.status}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Data Trends */}
        <div className="col-6">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Data Trends</h3>
            </div>
            <div className="trend-list">
              {dataTrends.map((trend, index) => (
                <div key={index} className="trend-item">
                  <div className="trend-icon">
                    {trend.trend === 'up' && '📈'}
                    {trend.trend === 'down' && '📉'}
                    {trend.trend === 'stable' && '➡️'}
                  </div>
                  <div className="trend-info">
                    <div className="trend-name">{trend.name}</div>
                    <div className="trend-meta">
                      <span className={`trend-change ${trend.trend}`}>{trend.change}</span>
                      <span className="trend-period">{trend.period}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Analytics Console */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Analytics Console</h3>
            </div>
            <div className="terminal console">
              <div className="console-line">{'>'} Analytics engine initialized</div>
              <div className="console-line">{'>'} Loading data sources...</div>
              <div className="console-line">{'>'} Processing 2.4M data points</div>
              <div className="console-line">{'>'} Generating trend analysis...</div>
              <div className="console-line">{'>'} Report generation complete</div>
              <div className="console-line">{'>'} Ready for new analysis requests</div>
              <div className="console-line">{'>'} _</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
