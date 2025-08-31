import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Auth.css';

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    role: 'USER',
    organization: '',
    badge_number: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const roles = [
    { value: 'USER', label: 'User' },
    { value: 'ANALYST', label: 'Analyst' },
    { value: 'MANAGER', label: 'Manager' },
    { value: 'ADMIN', label: 'Admin' },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
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
      
      // Mock registration
      if (formData.password === formData.password_confirm) {
        // Success - redirect to login
        navigate('/login');
      } else {
        setError('Passwords do not match');
      }
    } catch (err) {
      setError('Registration failed. Please try again.');
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
            <h1 className="glow-text">HACK2DRUG</h1>
            <p className="text-muted">Advanced Drug Detection & Monitoring System</p>
            <div className="auth-subtitle">
              <span className="terminal"> User Registration Terminal</span>
            </div>
          </div>

          {/* Registration Form */}
          <form onSubmit={handleSubmit} className="auth-form">
            {error && (
              <div className="alert alert-danger">
                <span className="alert-icon">⚠️</span>
                {error}
              </div>
            )}

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="first_name" className="form-label">
                  First Name
                </label>
                <input
                  type="text"
                  id="first_name"
                  name="first_name"
                  className="form-control"
                  value={formData.first_name}
                  onChange={handleChange}
                  placeholder="Enter your first name"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="last_name" className="form-label">
                  Last Name
                </label>
                <input
                  type="text"
                  id="last_name"
                  name="last_name"
                  className="form-control"
                  value={formData.last_name}
                  onChange={handleChange}
                  placeholder="Enter your last name"
                  required
                />
              </div>
            </div>

            <div className="form-row">
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
                  placeholder="Choose a username"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="email" className="form-label">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="form-control"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter your email"
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="role" className="form-label">
                  Role
                </label>
                <select
                  id="role"
                  name="role"
                  className="form-control"
                  value={formData.role}
                  onChange={handleChange}
                  required
                >
                  {roles.map((role) => (
                    <option key={role.value} value={role.value}>
                      {role.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="organization" className="form-label">
                  Organization
                </label>
                <input
                  type="text"
                  id="organization"
                  name="organization"
                  className="form-control"
                  value={formData.organization}
                  onChange={handleChange}
                  placeholder="Enter organization"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="badge_number" className="form-label">
                Badge Number
              </label>
              <input
                type="text"
                id="badge_number"
                name="badge_number"
                className="form-control"
                value={formData.badge_number}
                onChange={handleChange}
                placeholder="Enter badge number"
                required
              />
            </div>

            <div className="form-row">
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
                  placeholder="Create a password"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="password_confirm" className="form-label">
                  Confirm Password
                </label>
                <input
                  type="password"
                  id="password_confirm"
                  name="password_confirm"
                  className="form-control"
                  value={formData.password_confirm}
                  onChange={handleChange}
                  placeholder="Confirm your password"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="btn btn-primary auth-submit-btn"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  Creating Account...
                </>
              ) : (
                <>
                  <span className="btn-icon">👤</span>
                  Create Account
                </>
              )}
            </button>
          </form>

          {/* Footer Links */}
          <div className="auth-footer">
            <p className="text-center text-muted">
              Already have an account?{' '}
              <Link to="/login" className="auth-link">
                Sign In
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
            <span className="status-label">Registration:</span>
            <span className="status-value text-success">OPEN</span>
          </div>
          <div className="status-item">
            <span className="status-label">Security:</span>
            <span className="status-value text-success">ACTIVE</span>
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

export default Register;
