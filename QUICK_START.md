# 🚀 Quick Start Guide - Hack2Drug

Get the Hack2Drug detection system up and running in minutes!

## ⚡ Quick Setup (5 minutes)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Access the System
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/

## 🔑 Default Login
Use the superuser credentials you created:
- Username: (your superuser username)
- Password: (your superuser password)

## 🎯 What You'll See

### Backend (Django)
- ✅ Admin panel with all models
- ✅ REST API endpoints
- ✅ Database with sample data
- ✅ User management system

### Frontend (React)
- ✅ Modern dashboard with statistics
- ✅ User authentication (login/register)
- ✅ Navigation sidebar
- ✅ Responsive Material-UI design

## 🚨 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if port 8000 is free
- Ensure all dependencies are installed
- Verify virtual environment is activated

**Frontend won't start:**
- Check if port 3000 is free
- Ensure Node.js 16+ is installed
- Run `npm install` again

**Database errors:**
- Run `python manage.py migrate` again
- Check if SQLite file is writable

## 📱 Test the System

1. **Register a new user** at http://localhost:3000/register
2. **Login** with your credentials
3. **Explore the dashboard** and navigation
4. **Check the admin panel** at http://localhost:8000/admin/

## 🔧 Next Steps

1. **Configure environment variables** in `backend/config.env.example`
2. **Set up PostgreSQL** for production use
3. **Configure Redis** for caching and Celery
4. **Add your API keys** for social media monitoring
5. **Customize detection patterns** for your use case

## 📞 Need Help?

- Check the main README.md for detailed documentation
- Review the Django admin panel for data management
- Explore the API endpoints at http://localhost:8000/api-info/

---

**🎉 Congratulations!** You now have a fully functional drug detection platform running locally.
