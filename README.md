# MediTrack – Patient Medical Records Management System

A full-stack Django web application for managing patient medical records, prescriptions, and appointments. Built with modern DevOps practices including Docker containerization, Nginx reverse proxy, and CI/CD automation.

---

## Features

- **User Authentication** – Register, login, logout with Django's built-in auth system
- **Patient Management** – Full CRUD operations for patient profiles
- **Medical Records** – Create and view diagnosis records linked to patients
- **Prescriptions** – Multi-medication prescriptions with dosage and frequency tracking
- **Appointments** – Schedule and manage patient appointments with status tracking
- **Medications Catalogue** – Maintain a database of available medications
- **Dashboard** – Summary statistics with recent patients and upcoming appointments
- **Admin Panel** – Full Django admin with filters, search, and inline editing
- **Responsive Design** – Bootstrap 5 with custom styling

## Technologies Used

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Python 3.12 |
| Database | PostgreSQL 16 |
| Web Server | Nginx 1.25 |
| App Server | Gunicorn |
| Containerization | Docker (multi-stage build), Docker Compose |
| CI/CD | GitHub Actions |
| Frontend | Bootstrap 5, HTML5, CSS3 |
| Testing | pytest, pytest-django |
| Linting | flake8 |

## Database Schema

```
User (Django built-in)
 ├── Patient (FK: created_by)
 │    ├── MedicalRecord (FK: patient, FK: doctor→User)
 │    ├── Prescription (FK: patient, FK: doctor→User, M2M: medications)
 │    └── Appointment (FK: patient, FK: doctor→User)
 └── Medication (M2M via Prescription)
```

- **Many-to-One**: MedicalRecord → Patient, Appointment → Patient
- **Many-to-Many**: Prescription ↔ Medication

---

## Local Setup Instructions

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (for containerized setup)

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/00013219-CW-DSCC.git
cd 00013219-CW-DSCC

# Create environment file
cp .env.example .env
# Edit .env and set a strong SECRET_KEY and DATABASE_PASSWORD

# Build and start all services
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser (for admin panel)
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Access at http://localhost
```

### Option 2: Local Development (without Docker)

```bash
# Clone and enter directory
git clone https://github.com/YOUR_USERNAME/00013219-CW-DSCC.git
cd 00013219-CW-DSCC

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (uses SQLite by default)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
# Access at http://localhost:8000
```

---

## Deployment Instructions

### Server Setup (Ubuntu/Eskiz)

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Clone and deploy
git clone https://github.com/YOUR_USERNAME/00013219-CW-DSCC.git ~/meditrack
cd ~/meditrack
cp .env.example .env
nano .env  # Configure production values

docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

### SSL/HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `your-random-secret-key` |
| `DEBUG` | Debug mode (False for production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF | `https://yourdomain.com` |
| `DATABASE_NAME` | PostgreSQL database name | `meditrack` |
| `DATABASE_USER` | PostgreSQL username | `meditrack` |
| `DATABASE_PASSWORD` | PostgreSQL password | `strong-password` |
| `DATABASE_HOST` | Database host | `db` |
| `DATABASE_PORT` | Database port | `5432` |

---

## Running Tests

```bash
# With Docker
docker compose exec web pytest -v

# Local
pytest -v
```

## CI/CD Pipeline

The project uses GitHub Actions (`.github/workflows/deploy.yml`) with these stages:

1. **Lint** – flake8 code quality check
2. **Test** – pytest with PostgreSQL service container
3. **Build & Push** – Docker image to Docker Hub (tagged `latest` + commit SHA)
4. **Deploy** – SSH into server, pull image, restart services, run migrations

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `SSH_PRIVATE_KEY` | SSH private key for server access |
| `SSH_HOST` | Server IP or domain |
| `SSH_USERNAME` | SSH username on server |

---

## Screenshots

*Screenshots of the running application will be added here.*

---

## Test User Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin1234` |
| Doctor | `doctor1` | `doc1234!` |

---

## License

This project is submitted as coursework for the DSCC module.

Student ID: 00013219
