FROM python:3.10-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libaio1 libpq-dev

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY . .

# Collect static files (if applicable)
# RUN python manage.py collectstatic --noinput

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]
