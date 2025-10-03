# Production Deployment Guide

## Security Checklist

Before deploying to production, complete these essential security steps:

### 1. Change Secret Key
```python
# In app.py, replace:
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# With a secure random key:
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)
```

### 2. Use a Real Database
Replace the mock `users_db` dictionary with a proper database:

**Option A: SQLite (Simple)**
```python
import sqlite3
# Add user management with SQLite
```

**Option B: PostgreSQL (Recommended)**
```python
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

**Option C: MySQL/MariaDB**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/dbname'
```

### 3. Use Production WSGI Server

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### 4. Enable HTTPS
Use a reverse proxy (Nginx or Apache) with SSL/TLS:

**Nginx Configuration Example:**
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Environment Variables
Store sensitive configuration in environment variables:

```python
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
```

### 6. Implement Rate Limiting
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ... login logic
```

### 7. Add Logging
```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

### 8. Disable Debug Mode
```python
if __name__ == '__main__':
    app.run(debug=False)  # Never use debug=True in production
```

## Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

**Build and Run:**
```bash
docker build -t joresa-py-tools .
docker run -p 8000:8000 joresa-py-tools
```

## Environment Setup

Create a `.env` file (DO NOT commit to git):
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
FLASK_ENV=production
```

## Monitoring and Maintenance

1. **Set up monitoring** (e.g., Prometheus, Grafana)
2. **Configure backups** for your database
3. **Set up alerts** for errors and downtime
4. **Regular security updates** for dependencies
5. **Log rotation** to manage disk space

## Performance Optimization

1. Use caching (Redis, Memcached)
2. Enable compression
3. Optimize database queries
4. Use CDN for static files
5. Implement load balancing for high traffic

## Additional Security Measures

1. **CSRF Protection**: Already included with Flask
2. **SQL Injection Prevention**: Use parameterized queries
3. **XSS Protection**: Flask auto-escapes templates
4. **Secure Headers**: Add security headers with Flask-Talisman
5. **Two-Factor Authentication**: Consider adding 2FA for sensitive accounts

## Deployment Platforms

- **Heroku**: Easy deployment with git push
- **AWS**: EC2, Elastic Beanstalk, or ECS
- **Google Cloud**: App Engine or Cloud Run
- **DigitalOcean**: App Platform or Droplets
- **Azure**: App Service

## Support

For production issues:
1. Check application logs
2. Review server logs (Nginx/Apache)
3. Monitor database connections
4. Check disk space and memory usage
