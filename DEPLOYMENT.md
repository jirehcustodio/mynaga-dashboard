# MyNaga Dashboard - Deployment Guide

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker & Docker Compose installed
- Your data files ready

### Deploy with Docker Compose

1. **Navigate to project root:**
```bash
cd mynaga-dashboard
```

2. **Start all services:**
```bash
docker-compose up -d
```

3. **Access the application:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

4. **View logs:**
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

5. **Stop services:**
```bash
docker-compose down
```

---

## 🚀 Heroku Deployment (Backend)

### Prerequisites
- Heroku CLI installed
- Heroku account

### Deploy Backend

```bash
# Install Heroku CLI if not already done
# Then login
heroku login

# Create app
heroku create mynaga-dashboard-api

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Deploy Frontend (Pointing to Heroku Backend)

Update `frontend/src/services/api.js`:
```javascript
const API = axios.create({
  baseURL: 'https://mynaga-dashboard-api.herokuapp.com/api',
})
```

Then deploy to Vercel (see below).

---

## 🌐 Vercel Deployment (Frontend)

### Prerequisites
- Vercel account
- GitHub account

### Deploy Frontend

1. **Create `vercel.json` in frontend directory:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "VITE_API_URL": {
      "default": "https://mynaga-dashboard-api.herokuapp.com/api"
    }
  }
}
```

2. **Push to GitHub:**
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

3. **Deploy:**
- Visit `vercel.com`
- Click "Import Project"
- Select your GitHub repo
- Vercel will auto-detect and deploy
- Update environment variables if needed

---

## ☁️ AWS Deployment

### Backend (EC2 + RDS)

1. **Create EC2 instance:**
   - Ubuntu 20.04 LTS
   - t2.micro (free tier eligible)
   - Security group: Allow 80, 443, 8000

2. **SSH into instance:**
```bash
ssh -i key.pem ec2-user@your-instance-ip
```

3. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv git

# Clone repository
git clone your-repo-url
cd mynaga-dashboard/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

4. **Create RDS PostgreSQL database:**
   - DB instance class: db.t2.micro
   - Storage: 20GB
   - Enable Multi-AZ: No
   - Note the endpoint and credentials

5. **Update `.env` with RDS connection:**
```bash
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/mynaga_dashboard
ENVIRONMENT=production
DEBUG=false
```

6. **Run with Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

7. **Setup Nginx reverse proxy:**
```bash
sudo apt install nginx

# Create Nginx config at /etc/nginx/sites-available/mynaga
sudo vim /etc/nginx/sites-available/mynaga
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/mynaga /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

8. **Setup SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Frontend (CloudFront + S3)

1. **Create S3 bucket:**
   - Name: mynaga-dashboard
   - Block public access: OFF
   - Enable versioning

2. **Build and upload:**
```bash
cd frontend
npm run build

aws s3 sync dist/ s3://mynaga-dashboard/
```

3. **Create CloudFront distribution:**
   - Origin: Your S3 bucket
   - HTTPS only
   - Add SSL certificate

---

## 🔒 Environment Variables

### Backend

Create `.env` in backend directory:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/mynaga_dashboard
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
DEBUG=false
```

### Frontend

Create `.env` in frontend directory:
```
VITE_API_URL=https://api.yourdomain.com
```

---

## 📦 Production Checklist

- [ ] Database backups enabled
- [ ] SSL certificates installed
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] Environment variables set
- [ ] Logging enabled
- [ ] Monitoring setup (optional)
- [ ] Database migrations run
- [ ] Static files optimized
- [ ] Error tracking enabled (e.g., Sentry)

---

## 🔄 Continuous Deployment

### GitHub Actions (Automated Deployment)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          # Add your deployment script
          
      - name: Deploy Frontend
        run: |
          # Add your deployment script
```

---

## 🆘 Troubleshooting

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -h your-host -U username -d database_name

# Check backend logs
docker-compose logs backend
```

### CORS Errors
Update CORS settings in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### File Upload Issues
Check disk space and file permissions:
```bash
df -h  # Check disk space
ls -la /app/uploads  # Check permissions
```

---

## 📊 Monitoring & Logging

### Application Monitoring
- Set up CloudWatch (AWS) or Datadog
- Monitor API response times
- Track error rates
- Alert on failures

### Database Monitoring
- Enable slow query logs
- Monitor connection pool
- Setup automated backups
- Monitor disk usage

---

**🎉 Your MyNaga Dashboard is now live in production!**
