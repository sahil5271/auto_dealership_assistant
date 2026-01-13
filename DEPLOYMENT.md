# Deployment Guide

## Local Development

### 1. Setup Python Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run in Development Mode
```bash
# Text-based (default)
python main.py

# With voice
python main.py --voice

# API Server
python main.py --api

# Run tests
python main.py --test
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t auto-dealership-assistant:latest .
```

### Run Single Container
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e VOICE_PROVIDER=local \
  auto-dealership-assistant:latest python main.py --api
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Cloud Deployment

### AWS EC2
```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. Connect via SSH
# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone repository
git clone https://github.com/yourusername/auto_dealership_assistant.git
cd auto_dealership_assistant

# 5. Set environment
cp .env.example .env
# Edit .env with your keys

# 6. Run with Docker Compose
docker-compose up -d
```

### Heroku
```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create your-app-name

# 4. Set environment variables
heroku config:set OPENAI_API_KEY=your_key

# 5. Deploy
git push heroku main
```

### Google Cloud Run
```bash
# 1. Install gcloud CLI
# 2. Build image
gcloud builds submit --tag gcr.io/your-project/auto-dealership

# 3. Deploy
gcloud run deploy auto-dealership \
  --image gcr.io/your-project/auto-dealership \
  --platform managed \
  --set-env-vars OPENAI_API_KEY=your_key
```

## Performance Optimization

### Caching
- Implement Redis for conversation caching
- Cache car inventory in memory

### Database
- Use PostgreSQL for production bookings
- Implement connection pooling

### API
- Add rate limiting
- Use async endpoints
- Implement caching headers

### Monitoring
```bash
# Add monitoring with Prometheus/Grafana
# Add error tracking with Sentry
# Add APM with New Relic
```

## Security Checklist

- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Implement API rate limiting
- [ ] Validate all inputs
- [ ] Use CORS properly
- [ ] Implement authentication/authorization
- [ ] Keep dependencies updated
- [ ] Use security headers
- [ ] Enable audit logging
- [ ] Regular security audits

## Scaling

### Horizontal Scaling
```bash
# Run multiple API instances behind load balancer
docker-compose scale api=3
```

### Vertical Scaling
- Use larger instances
- Increase memory/CPU
- Optimize database queries

### Database Scaling
- Implement read replicas
- Use connection pooling
- Optimize indexes

## Monitoring & Logging

### Logs
- Application logs to stdout
- Access logs with Nginx
- Error tracking with Sentry

### Metrics
- API response times
- Error rates
- Agent performance
- Booking success rates

### Health Checks
```bash
# Check API health
curl http://localhost:8000/health

# Check database
curl http://localhost:8000/api/v1/cars

# WebSocket health
wscat -c ws://localhost:8000/ws/chat/test
```

## Troubleshooting

### High Memory Usage
- Check conversation memory limits
- Implement memory caching strategy
- Use smaller models

### Slow API Response
- Check LLM API latency
- Implement response caching
- Use async processing

### Database Issues
- Check connection limits
- Monitor query performance
- Review indexes
