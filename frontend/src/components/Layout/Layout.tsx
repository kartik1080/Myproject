import React from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import './Layout.css';

const Layout: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/detection', label: 'Detection', icon: '🔍' },
    { path: '/monitoring', label: 'Monitoring', icon: '📡' },
    { path: '/analytics', label: 'Analytics', icon: '📈' },
    { path: '/users', label: 'Users', icon: '👥' },
  ];

  const handleLogout = () => {
    // Clear authentication data
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="layout">
      {/* Navigation Header */}
      <nav className="nav">
        <div className="container">
          <div className="nav-content">
            <Link to="/dashboard" className="nav-brand glow-text">
              EchoBat
            </Link>
            
            <div className="nav-menu">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </div>

            <div className="nav-actions">
              <button onClick={handleLogout} className="btn btn-danger">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          <Outlet />
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <p className="text-center text-muted">
              © 2025 Hack2Drug | Advanced Drug Detection & Monitoring System
            </p>
            <div className="footer-links">
              <span className="terminal">System Status: ONLINE</span>
              <span className="terminal">Version: 2.0.1</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
