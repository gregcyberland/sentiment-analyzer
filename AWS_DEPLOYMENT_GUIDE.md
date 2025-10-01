# AWS EC2 Deployment Guide for Sentiment Analyzer

## Security Group Configuration

### Required Ports (Inbound Rules):
- **Port 22**: SSH access (from your IP only)
- **Port 80**: HTTP access (0.0.0.0/0) - redirects to HTTPS
- **Port 443**: HTTPS access (0.0.0.0/0) - main application access
- **Port 8000**: Optional - Direct API access for debugging (your IP only)

## Deployment Steps

### 1. EC2 Instance Setup
```bash
# Connect to your EC2 instance
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Update the system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Deploy Your Application
```bash
# Clone your repository or upload files
git clone https://github.com/gregcyberland/sentiment-analyzer.git
cd sentiment-analyzer

# Create .env file with your credentials
nano .env
```

### 3. Environment Variables (.env file)
```
OPENAI_API_KEY=your_openai_api_key_here
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_app_password_here
```

### 4. Build and Run
```bash
# Build and start the services
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs if needed
docker-compose logs -f
```

## Access Your Application

### HTTPS Access (Recommended):
```
https://YOUR_EC2_IP
```

### HTTP Access (Auto-redirects to HTTPS):
```
http://YOUR_EC2_IP
```

### Direct API Access (for debugging):
```
http://YOUR_EC2_IP:8000
```

## API Endpoints

### Health Check:
```bash
curl -k https://YOUR_EC2_IP/
```

### Sentiment Analysis:
```bash
curl -k -X POST https://YOUR_EC2_IP/analyze \
  -H "Content-Type: application/json" \
  -d '{"text_to_analyze": "I am feeling great today!"}'
```

### Message Enhancement:
```bash
curl -k -X POST https://YOUR_EC2_IP/enhance \
  -H "Content-Type: application/json" \
  -d '{"message_to_enhance": "thx for the help"}'
```

## SSL Certificate Note

The current configuration uses Caddy's internal TLS, which generates a self-signed certificate. Browsers will show a security warning that you can bypass by clicking "Advanced" and "Proceed to site".

For production use with a domain name, consider:
1. Getting a domain name
2. Using Let's Encrypt certificates via Caddy
3. Updating the Caddyfile to use your domain

## Troubleshooting

### Check service status:
```bash
docker-compose ps
```

### View logs:
```bash
docker-compose logs caddy
docker-compose logs message-correction-api
```

### Restart services:
```bash
docker-compose restart
```

### Check if ports are open:
```bash
netstat -tlnp | grep -E ':(80|443|8000)'
```

## Security Considerations

1. **Firewall**: Only open necessary ports in AWS Security Groups
2. **SSH Access**: Restrict SSH access to your IP only
3. **API Access**: Consider adding authentication for production use
4. **Environment Variables**: Keep sensitive data in .env file, never commit to git
5. **Updates**: Regularly update Docker images and dependencies