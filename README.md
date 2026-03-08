# AS Drones - Aerial Site Intelligence 🚁

[![Django Version](https://img.shields.io/badge/django-6.0.1-green)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)

This is my website for my Drone Services business. Check out [asdrones.io](https://asdrones.io)

## Quick Start

### Local Development with Docker

```bash
# Clone the repository
git clone https://github.com/anthonysawyer94/asdrones.git
cd asdrones

# Start Docker containers (creates PostgreSQL, Redis, and Django)
docker-compose up --build

# In another terminal, set up the database
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Visit http://localhost:8000

---

## Development

### Without Docker (Legacy)

```bash
# Clone and set up virtual environment
git clone https://github.com/anthonysawyer94/asdrones.git
cd asdrones
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/dev.txt

# Set up database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## Production

### Automated Deployment (GitHub Actions)

Deployment happens automatically when you push to the `main` branch.

1. Push to `main` branch
2. GitHub Actions builds the Docker image
3. EC2 server pulls the latest code and restarts containers

**Required GitHub Secrets:**

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `EC2_HOST` | EC2 public IP address |
| `EC2_SSH_KEY` | Private SSH key (.pem file contents) |
| `EC2_USERNAME` | SSH username (usually `ubuntu`) |

### Manual Deployment

```bash
# SSH into your server
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Navigate to project directory
cd /var/www/asdrones

# Pull latest code
sudo git fetch origin main
sudo git reset --hard origin/main

# Restart containers
sudo docker-compose -f docker-compose.prod.yml down
sudo docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
sudo docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
```

---

## Environment Variables

### Local Development (.env.local)

Create a `.env.local` file in the project root:

```env
DEBUG=True
DJANGO_SETTINGS_MODULE=asdrones.conf.prod
SECRET_KEY=dev-secret-key
PRODUCTION_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_PASSWORD=devpassword123
REDIS_URL=redis://redis:6379/1
```

### Production (.env)

On your EC2 server, create a `.env` file with production values:

```env
DEBUG=False
DJANGO_SETTINGS_MODULE=asdrones.conf.prod
SECRET_KEY=your-production-secret-key
PRODUCTION_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_PASSWORD=secure-database-password
REDIS_URL=redis://redis:6379/1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
NOTIFY_EMAIL=your-email@gmail.com
```

---

## Docker Services

| Service | Description | Port |
|---------|-------------|------|
| web | Django application | 8000 |
| db | PostgreSQL database | 5432 |
| redis | Redis cache | 6379 |

---

## Useful Commands

```bash
# Local development
docker-compose up --build          # Start containers
docker-compose down                # Stop containers
docker-compose exec web python manage.py migrate  # Run migrations

# Production (on EC2)
sudo docker-compose -f docker-compose.prod.yml up -d --build  # Deploy
sudo docker-compose -f docker-compose.prod.yml logs -f        # View logs
sudo docker-compose -f docker-compose.prod.yml restart        # Restart
```
