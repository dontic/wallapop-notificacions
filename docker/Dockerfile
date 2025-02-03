# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-bullseye

# Expose port 8000
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install pipenv
RUN pip install -U pipenv

# Copy only the files needed for installing dependencies
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv requirements > requirements.txt && \
    pip install -r requirements.txt && \
    rm -rf Pipfile Pipfile.lock requirements.txt

# Copy project files
COPY core/ ./core/
COPY monitor/ ./monitor/
COPY manage.py ./
COPY docker/entrypoints/ ./docker/entrypoints/

# Make entrypoint scripts executable
RUN chmod +x /app/docker/entrypoints/*.sh

# Default entrypoint
ENTRYPOINT ["/app/docker/entrypoints/entrypoint-django.sh"]