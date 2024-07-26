FROM nginx:latest

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for Certbot challenges
RUN mkdir -p /var/www/certbot

# Install Certbot and dependencies
RUN apt install certbot python3-certbot-nginx
