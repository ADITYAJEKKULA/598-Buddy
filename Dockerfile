# Use the specific Python version from your example
FROM python:3.12.6

# Set environment variables
ENV PYTHONUNBUFFERED 1
# Ensure this matches the python path to your settings.py
# Likely 'backend.settings' based on your structure
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Set the working directory in the container
WORKDIR /

# Copy requirements.txt to the root
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Create the /app directory
RUN mkdir /app

# Copy the entire project to /app
COPY . /app/

# Set the working directory to /app
WORKDIR /app

# Set execute permissions
RUN chmod +x /app/docker_server.sh

# Expose the port
EXPOSE 80

# Set entrypoint
ENTRYPOINT ["/app/docker_server.sh"]