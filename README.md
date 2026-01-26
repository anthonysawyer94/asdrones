# AS Drones - Aerial Site Intelligence 🚁

[![Django Version](https://img.shields.io/badge/django-6.0.1-green)](https://www.djangoproject.com/)

This is my website for my Drone Services. I would like to thank Bobby's [youtube video](https://www.youtube.com/watch?v=IsAjtRfw8ps) for showing me how to create a production ready Django project. Before it was a mess testing my code. I do so many commits to prod because I didn't have a dev envionment that worked on my local set up. Check out my [website](https://asdrones.io)

### 1. Requirements

- Python 3.11+
- Virtual Environment (`venv`)

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/anthonysawyer94/asdrones.git

# Go to directory
cd asdrones

# Copy Environment Variables
cp .env.dev .env
echo "" >> .env
cat .env.prod >> .env

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip3 install -r requirements/dev.txt
pip3 install -r requirements/prod.txt

# Set up Database (this creates the db from models.py)
python3 manage.py makemigrations
python3 manage.prod.py migrate

# *Before running Prod, get all static files in one single folder
python3 manage.prod.py collectstatic

#run django project
python3 manage.py runserver # For Dev
python3 manage.prod.py runserver # For Prod
```
