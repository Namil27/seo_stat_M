FROM nginx:latest

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for Certbot challenges
RUN mkdir -p /var/www/certbot

# Install Certbot and its dependencies
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    curl \
    gnupg && \
    # Add Certbot repository key
    curl -fsSL https://dl.eff.org/certbot-auto.asc | apt-key add - && \
    # Add Certbot repository
    echo "deb http://ppa.launchpad.net/certbot/certbot/ubuntu focal main" > /etc/apt/sources.list.d/certbot.list && \
    apt-get update && \
    apt-get install -y \
    certbot \
    python3-certbot-nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
