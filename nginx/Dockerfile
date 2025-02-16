# Use the official Nginx base image
FROM nginx:alpine

# Set the working directory inside the container (optional)
WORKDIR /etc/nginx

# Copy the custom nginx.conf file to the container's Nginx configuration directory
COPY ./nginx.conf /etc/nginx/nginx.conf

# Expose the port (commonly 80 for HTTP, 443 for HTTPS)
EXPOSE 80
