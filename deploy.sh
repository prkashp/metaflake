#!/bin/bash

# Variables
INSTANCE_ID="<INSTANCE_ID>"  # Replace with the instance ID from CloudFormation output
KEY_FILE="<PATH_TO_YOUR_KEY_FILE.pem>"  # Replace with the path to your SSH key file
USER="ec2-user"  # or "ubuntu" for Ubuntu instances
REGION="<AWS_REGION>"  # e.g., us-east-1

# Get the private IP of the EC2 instance
INSTANCE_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query "Reservations[*].Instances[*].PrivateIpAddress" --output text --region $REGION)

# SSH into the EC2 instance
ssh -i "$KEY_FILE" "$USER@$INSTANCE_IP" << 'EOF'
  # Update and install Docker
  sudo yum update -y
  sudo amazon-linux-extras install docker -y
  sudo service docker start
  sudo systemctl enable docker

  # Pull and run Docker container
  docker pull your-dockerhub-username/your-image-name  # Replace with your Docker image
  docker run -d -p 80:80 -p 443:443 your-dockerhub-username/your-image-name

  # Install Nginx for SSL termination (optional)
  sudo amazon-linux-extras install nginx1 -y
  sudo service nginx start
  sudo systemctl enable nginx

  # Set up SSL certificate (self-signed or from internal CA)
  sudo mkdir -p /etc/nginx/ssl
  sudo openssl req -newkey rsa:2048 -nodes -keyout /etc/nginx/ssl/nginx.key -x509 -days 365 -out /etc/nginx/ssl/nginx.crt

  # Configure Nginx to use SSL
  echo '
  server {
      listen 443 ssl;
      server_name your-internal-domain.local;  # Replace with your internal domain

      ssl_certificate /etc/nginx/ssl/nginx.crt;
      ssl_certificate_key /etc/nginx/ssl/nginx.key;

      location / {
          proxy_pass http://localhost:80;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }

  server {
      listen 80;
      server_name your-internal-domain.local;

      location / {
          proxy_pass http://localhost:80;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  ' | sudo tee /etc/nginx/nginx.conf

  # Restart Nginx
  sudo systemctl restart nginx

  # Update /etc/hosts or internal DNS to resolve your internal domain
  echo "$INSTANCE_IP your-internal-domain.local" | sudo tee -a /etc/hosts
EOF

echo "Deployment complete. Access your application at https://your-internal-domain.local"
