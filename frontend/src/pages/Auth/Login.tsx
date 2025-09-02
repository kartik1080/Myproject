import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Auth.css';

const Login: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock authentication
      if (formData.username === 'admin' && formData.password === 'admin') {
        localStorage.setItem('token', 'mock-jwt-token');
        localStorage.setItem('user', JSON.stringify({
          username: 'admin',
          role: 'admin',
          first_name: 'System',
          last_name: 'Administrator'
        }));
        navigate('/dashboard');
      } else {
        setError('Invalid credentials. Try admin/admin');
      }
    } catch (err) {
      setError('Authentication failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      {/* Matrix Rain Background */}
      <div className="matrix-bg" id="matrix-bg"></div>
      
      <div className="auth-content">
        <div className="auth-card">
          {/* Header */}
          <div className="auth-header">
            <h1 className="glow-text">EchoBat</h1>
            <p className="text-muted">Advanced Drug Detection & Monitoring System</p>
            <div className="auth-subtitle">
              <span className="terminal"> Access Control Terminal</span>
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="auth-form">
            {error && (
              <div className="alert alert-danger">
                <span className="alert-icon">⚠️</span>
                {error}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="username" className="form-label">
                Username
              </label>
              <input
                type="text"
                id="username"
                name="username"
                className="form-control"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter your username"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                className="form-control"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary auth-submit-btn"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  Authenticating...
                </>
              ) : (
                <>
                  <span className="btn-icon">🔐</span>
                  Access System
                </>
              )}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="demo-credentials">
            <div className="terminal">
              <span className="terminal-prompt"></span>
              <span className="terminal-text">Demo Credentials: admin / admin</span>
            </div>
          </div>

          {/* Footer Links */}
          <div className="auth-footer">
            <p className="text-center text-muted">
              Don't have access?{' '}
              <Link to="/register" className="auth-link">
                Contact System Administrator
              </Link>
            </p>
          </div>
        </div>

        {/* System Status */}
        <div className="system-status-panel">
          <div className="status-item">
            <span className="status-label">System:</span>
            <span className="status-value text-success">ONLINE</span>
          </div>
          <div className="status-item">
            <span className="status-label">Security:</span>
            <span className="status-value text-success">ACTIVE</span>
          </div>
          <div className="status-item">
            <span className="status-label">Database:</span>
            <span className="status-value text-success">CONNECTED</span>
          </div>
          <div className="status-item">
            <span className="status-label">Version:</span>
            <span className="status-value text-blue">2.0.1</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
