# ============================================================
# Dockerfile for CloudTask - Flask Task Manager Application
# Phase 2: Dockerization
# ============================================================

# Step 1: Use an official Python base image (lightweight "slim" version)
# "slim" means it has only the essentials — keeps our image small
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
# All commands after this will run from /app inside the container
WORKDIR /app

# Step 3: Copy the requirements file first (for better caching)
# Docker caches each step. If requirements.txt hasn't changed,
# Docker won't re-install packages — saving build time
COPY requirements.txt .

# Step 4: Install Python dependencies
# --no-cache-dir  = don't store pip's download cache (keeps image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . .

# Step 6: Expose port 5000 so we can access Flask from outside the container
EXPOSE 5000

# Step 7: Run the Flask application when the container starts
CMD ["python", "app.py"]
