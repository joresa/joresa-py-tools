# Production Deployment Guide

This guide covers deploying JoResa Python Tools to production environments.

## Pre-Deployment Checklist

- [ ] All tests pass (see TESTING.md)
- [ ] Security review completed
- [ ] Database backups configured
- [ ] Environment variables set
- [ ] SSL/TLS certificates ready
- [ ] Domain configured
- [ ] Monitoring set up

## Environment Variables

Create a `.env` file (never commit this!):

```bash
# Secret key - MUST be changed for production
SECRET_KEY=your-secure-random-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/joresa_tools

# Flask environment
FLASK_ENV=production
FLASK_DEBUG=False

# Optional: Email configuration (for future features)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

### Generate a Secure Secret Key

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

## Database Setup

### Option 1: PostgreSQL (Recommended)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE joresa_tools;
CREATE USER joresa_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE joresa_tools TO joresa_user;
\q

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://joresa_user:secure_password@localhost:5432/joresa_tools
```

### Option 2: MySQL

```bash
# Install MySQL
sudo apt-get install mysql-server

# Create database
mysql -u root -p
CREATE DATABASE joresa_tools;
CREATE USER 'joresa_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON joresa_tools.* TO 'joresa_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Update DATABASE_URL in .env
DATABASE_URL=mysql://joresa_user:secure_password@localhost:3306/joresa_tools
```

### Initialize Database

```bash
python init_db.py
```

## Deployment Options

### Option 1: Traditional Server (Ubuntu)

#### 1. Install System Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install python3 python3-pip python3-venv nginx supervisor -y
```

#### 2. Set Up Application

```bash
# Create app directory
sudo mkdir -p /var/www/joresa-tools
cd /var/www/joresa-tools

# Clone repository
git clone https://github.com/joresa/joresa-py-tools.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Set up environment
cp .env.example .env
# Edit .env with production values
nano .env

# Initialize database
python init_db.py

# Create instance directory
mkdir -p instance
```

#### 3. Configure Gunicorn

Create `/var/www/joresa-tools/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/joresa-tools/error.log"
accesslog = "/var/log/joresa-tools/access.log"
loglevel = "info"
```

#### 4. Configure Supervisor

Create `/etc/supervisor/conf.d/joresa-tools.conf`:

```ini
[program:joresa-tools]
directory=/var/www/joresa-tools
command=/var/www/joresa-tools/venv/bin/gunicorn -c gunicorn_config.py "app:create_app()"
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/joresa-tools/supervisor-error.log
stdout_logfile=/var/log/joresa-tools/supervisor-access.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/joresa-tools
sudo chown www-data:www-data /var/log/joresa-tools

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start joresa-tools
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/joresa-tools`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static {
        alias /var/www/joresa-tools/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/joresa-tools /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. Set Up SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already configured by Certbot)
sudo systemctl status certbot.timer
```

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create instance directory
RUN mkdir -p instance

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://joresa:password@db:5432/joresa_tools
      - FLASK_ENV=production
    depends_on:
      - db
    volumes:
      - ./instance:/app/instance

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=joresa_tools
      - POSTGRES_USER=joresa
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - web

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose up -d
```

### Option 3: Cloud Platforms

#### Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create joresa-tools

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Initialize database
heroku run python init_db.py
```

Create `Procfile`:
```
web: gunicorn "app:create_app()" --workers 4
```

#### AWS Elastic Beanstalk

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init -p python-3.11 joresa-tools`
3. Create environment: `eb create joresa-tools-env`
4. Set environment variables in AWS Console
5. Deploy: `eb deploy`

#### DigitalOcean App Platform

1. Connect GitHub repository
2. Configure build settings
3. Add environment variables
4. Deploy automatically on push

## Security Hardening

### 1. Update config.py for Production

```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Security settings
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
```

### 2. Regular Updates

```bash
# Update dependencies regularly
pip list --outdated
pip install --upgrade -r requirements.txt
```

### 3. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
```

## Monitoring and Logging

### 1. Application Logging

Update `run.py`:

```python
import logging
from logging.handlers import RotatingFileHandler
import os

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/joresa-tools.log', 
                                      maxBytes=10240000, 
                                      backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('JoResa Tools startup')
```

### 2. Error Monitoring

Consider integrating:
- Sentry for error tracking
- New Relic for performance monitoring
- Datadog for infrastructure monitoring

## Backup Strategy

### Database Backups

```bash
# PostgreSQL
pg_dump joresa_tools > backup_$(date +%Y%m%d).sql

# Automated daily backups
cat > /etc/cron.daily/backup-joresa-db << 'EOF'
#!/bin/bash
pg_dump joresa_tools > /backups/joresa_$(date +%Y%m%d).sql
find /backups -mtime +30 -delete
EOF
chmod +x /etc/cron.daily/backup-joresa-db
```

## Performance Optimization

1. **Use CDN for static files**
2. **Enable gzip compression** in Nginx
3. **Configure caching** for static assets
4. **Database indexing** on frequently queried fields
5. **Connection pooling** for database

## Troubleshooting

### Application Won't Start
```bash
# Check supervisor logs
sudo tail -f /var/log/joresa-tools/supervisor-error.log

# Check application logs
tail -f /var/log/joresa-tools/error.log
```

### Database Connection Errors
- Verify DATABASE_URL is correct
- Check database is running
- Verify user permissions

### Permission Issues
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/joresa-tools
sudo chmod -R 755 /var/www/joresa-tools
```

## Maintenance

### Updates

```bash
# Pull latest code
cd /var/www/joresa-tools
git pull origin main

# Install new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations if needed
python init_db.py

# Restart application
sudo supervisorctl restart joresa-tools
```

### Monitoring

- Check logs daily
- Monitor disk space
- Review database size
- Check SSL certificate expiry
- Monitor application performance

## Support

For production issues:
1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Contact maintainers

## Additional Resources

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
