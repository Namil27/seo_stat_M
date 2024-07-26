FROM nginx:latest

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for Certbot challenges
RUN mkdir -p /var/www/certbot

# Install dependencies and Certbot using snapd
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    snapd && \
    # Install Certbot using snapd
    snap install core && \
    snap refresh core && \
    snap install --classic certbot && \
    # Make Certbot command available
    ln -s /snap/bin/certbot /usr/bin/certbot && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
