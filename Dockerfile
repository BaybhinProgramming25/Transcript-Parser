# Use an official Nginx runtime as a parent image
FROM nginx:latest

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Add our configuration file
COPY configs/default.conf /etc/nginx/conf.d/

# Copy your custom index.html file to Nginx server
COPY client/index.html /usr/share/nginx/html

# Expose ports
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]