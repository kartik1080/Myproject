# Hack2Drug Detection System

A comprehensive, full-stack platform for detecting drug sales, exchange, and trading activities on encrypted platforms using advanced AI-powered detection and real-time monitoring.

## 🚀 Features

### Core Functionality
- **Real-time Drug Detection**: AI-powered pattern recognition for drug-related activities
- **Multi-Platform Monitoring**: Support for Telegram, Instagram, Twitter, and other encrypted platforms
- **Advanced Analytics**: Comprehensive reporting and trend analysis
- **User Management**: Role-based access control with admin, manager, analyst, and user roles
- **Real-time Alerts**: Instant notifications for suspicious activities
- **API Integration**: RESTful API with webhook support for third-party integrations

### Technical Features
- **Django Backend**: Robust REST API with Django REST Framework
- **React Frontend**: Modern, responsive UI with Material-UI components
- **Real-time Communication**: WebSocket support for live updates
- **Machine Learning**: Integration with scikit-learn and TensorFlow for pattern detection
- **Database**: PostgreSQL with optimized queries and indexing
- **Caching**: Redis for performance optimization
- **Task Queue**: Celery for background processing
- **Security**: JWT authentication, role-based permissions, audit logging

## 🏗️ Architecture

```
Hack2Drug/
├── backend/                 # Django backend
│   ├── hack2drug/          # Main project settings
│   ├── users/              # User management app
│   ├── detection/          # Drug detection app
│   ├── monitoring/         # Platform monitoring app
│   ├── analytics/          # Analytics and reporting app
│   ├── api/                # API management app
│   ├── static/             # Static files
│   ├── media/              # Media uploads
│   ├── logs/               # Application logs
│   └── ml_models/          # Machine learning models
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── store/          # Redux store and slices
│   │   └── services/       # API services
│   └── public/             # Public assets
└── docs/                   # Documentation
```

## 🛠️ Technology Stack

### Backend
- **Django 4.2+**: Web framework
- **Django REST Framework**: API framework
- **PostgreSQL**: Primary database
- **Redis**: Caching and message broker
- **Celery**: Background task processing
- **Channels**: WebSocket support
- **JWT**: Authentication
- **scikit-learn/TensorFlow**: Machine learning

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Material-UI**: Component library
- **Redux Toolkit**: State management
- **React Router**: Navigation
- **Formik + Yup**: Form handling and validation
- **Chart.js**: Data visualization

### DevOps
- **Docker**: Containerization
- **Nginx**: Web server
- **Gunicorn**: WSGI server
- **Daphne**: ASGI server

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Hack2Drug
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/hack2drug
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### Start Backend Server
```bash
python manage.py runserver
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm start
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api-info/

## 🔐 Authentication

The system uses JWT (JSON Web Tokens) for authentication:

1. **Register**: Create a new account with role assignment
2. **Login**: Authenticate with username/password
3. **Token Management**: Automatic token refresh and management
4. **Role-based Access**: Different permissions based on user roles

### User Roles
- **Admin**: Full system access and user management
- **Manager**: Organization-level access and team management
- **Analyst**: Detection review and analysis capabilities
- **User**: Basic access to assigned detections

## 📊 API Endpoints

### Authentication
- `POST /users/register/` - User registration
- `POST /users/login/` - User authentication
- `POST /users/logout/` - User logout
- `GET /users/me/` - Current user info

### Detection
- `GET /detection/` - List detections
- `POST /detection/` - Create detection
- `GET /detection/{id}/` - Detection details
- `PUT /detection/{id}/` - Update detection
- `POST /detection/{id}/review/` - Review detection

### Monitoring
- `GET /monitoring/` - List monitoring sessions
- `POST /monitoring/` - Create monitoring session
- `GET /monitoring/{id}/` - Session details
- `POST /monitoring/{id}/start/` - Start monitoring

### Analytics
- `GET /analytics/` - List reports
- `POST /analytics/reports/` - Generate report
- `GET /analytics/dashboard/` - Dashboard data
- `GET /analytics/trends/` - Trend analysis

## 🔧 Configuration

### Backend Settings
Key configuration options in `backend/hack2drug/settings.py`:

- **Database**: Configure PostgreSQL connection
- **Redis**: Set up caching and Celery broker
- **JWT**: Authentication token settings
- **CORS**: Cross-origin resource sharing
- **File Uploads**: Media and static file handling
- **Logging**: Application logging configuration

### Frontend Configuration
Environment variables in `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws/
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Setup
1. **Environment Variables**: Configure production settings
2. **Database**: Set up production PostgreSQL instance
3. **Redis**: Configure production Redis server
4. **Static Files**: Collect and serve static files
5. **Web Server**: Configure Nginx with Gunicorn/Daphne

### Docker Deployment
```bash
docker-compose up -d
```

## 📈 Monitoring & Analytics

### System Health
- Real-time system performance metrics
- Database connection monitoring
- API response time tracking
- Error rate monitoring

### User Analytics
- User activity tracking
- Feature usage statistics
- Performance metrics
- Audit logging

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Granular permission system
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: ORM-based queries
- **XSS Protection**: Content Security Policy
- **CSRF Protection**: Cross-site request forgery prevention
- **Rate Limiting**: API request throttling
- **Audit Logging**: Complete user action tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Roadmap

### Phase 1 (Current)
- ✅ Basic user authentication
- ✅ Core detection models
- ✅ Basic monitoring system
- ✅ User management

### Phase 2 (Next)
- 🔄 Advanced ML models
- 🔄 Real-time WebSocket updates
- 🔄 Advanced analytics dashboard
- 🔄 Mobile app

### Phase 3 (Future)
- 📋 AI-powered threat detection
- 📋 Integration with law enforcement APIs
- 📋 Advanced reporting tools
- 📋 Multi-language support

---

**Note**: This is a comprehensive drug detection platform designed for law enforcement and regulatory compliance. Ensure all usage complies with local laws and regulations.
