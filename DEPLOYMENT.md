# 🚀 Verity AI - Deployment Guide

## Overview

This guide covers deploying the modernized Verity AI system with:
- **Unified Python FastAPI backend** (SQLite database)
- **React frontend** with TanStack Router
- **Blockchain integration** for immutable audit trails
- **Real-time WebSocket** updates
- **Comprehensive monitoring** with Prometheus & Grafana

---

## 📋 Prerequisites

### Required Software
- Docker & Docker Compose (v2.0+)
- Node.js 20+ (for local development)
- Python 3.10+ (for local development)
- Git

### Required Accounts/Services
- Google Cloud Platform (for Vision API)
- Docker Hub (for image registry)
- Domain name (for production)
- SSL certificate (Let's Encrypt recommended)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Frontend)                      │
│                  Port 80/443 (HTTPS)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                    │
│                    Port 5000                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │ • JWT Authentication                              │  │
│  │ • Document OCR (Google Vision)                    │  │
│  │ • Loan Verification Engine                        │  │
│  │ • WebSocket Real-time Updates                     │  │
│  │ • Blockchain Integration                          │  │
│  └──────────────────────────────────────────────────┘  │
└──────────┬────────────────┬────────────────┬───────────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  SQLite  │    │  Redis   │    │ Ganache  │
    │ Database │    │  Cache   │    │Blockchain│
    └──────────┘    └──────────┘    └──────────┘
```

---

## 🔧 Configuration

### 1. Environment Variables

Create `.env` file in `ai-service/`:

```bash
# Server
HOST=0.0.0.0
PORT=5000
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database
DATABASE_URL=sqlite+aiosqlite:////data/verity_ai.db

# JWT
JWT_SECRET=your-super-secret-jwt-key-min-32-chars-CHANGE-THIS
JWT_ALGORITHM=HS256
JWT_EXPIRES_IN=7d

# Google Cloud Vision
GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json
GCP_PROJECT_ID=your-gcp-project-id

# Blockchain
BLOCKCHAIN_NETWORK=ganache
BLOCKCHAIN_RPC_URL=http://ganache:8545
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
CONTRACT_ADDRESS=0xYOUR_CONTRACT_ADDRESS
ENABLE_BLOCKCHAIN=true

# Redis
REDIS_URL=redis://redis:6379/0
ENABLE_REDIS=true

# Monitoring
PROMETHEUS_ENABLED=true
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
ENABLE_SENTRY=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

### 2. Google Cloud Setup

1. Create a GCP project
2. Enable Cloud Vision API
3. Create a service account
4. Download JSON key file as `service-account-key.json`
5. Place in `ai-service/` directory

### 3. Blockchain Setup

#### Local Development (Ganache)
```bash
# Ganache starts automatically with docker-compose
# Default RPC: http://localhost:8545
# Chain ID: 1337
```

#### Deploy Smart Contract
```bash
cd ai-service
npm install -g truffle
truffle compile
truffle migrate --network development
# Copy contract address to .env
```

#### Production (Polygon/BSC)
```bash
# Update .env
BLOCKCHAIN_NETWORK=polygon
BLOCKCHAIN_RPC_URL=https://polygon-rpc.com
BLOCKCHAIN_PRIVATE_KEY=0xYOUR_PRODUCTION_KEY
```

---

## 🐳 Docker Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/verity-ai.git
cd verity-ai

# Create environment file
cp ai-service/.env.example ai-service/.env
# Edit .env with your values

# Add Google Cloud credentials
cp /path/to/your/service-account-key.json ai-service/

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Check health
curl http://localhost:5000/api/health
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 80, 443 | React app with Nginx |
| Backend | 5000 | FastAPI Python service |
| Redis | 6379 | Cache & real-time |
| Ganache | 8545 | Local blockchain |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Monitoring dashboard |

### Useful Commands

```bash
# View logs
docker-compose logs -f [service_name]

# Restart service
docker-compose restart backend

# Rebuild after code changes
docker-compose up -d --build backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Scale backend
docker-compose up -d --scale backend=3
```

---

## 🔐 SSL/HTTPS Setup

### Using Let's Encrypt

1. Install Certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. Obtain certificate:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. Update `nginx.conf`:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of config
}
```

4. Auto-renewal:
```bash
sudo certbot renew --dry-run
```

---

## 📊 Monitoring Setup

### Prometheus

Access: `http://localhost:9090`

Metrics available:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `verifications_total` - Loan verifications
- `blockchain_transactions_total` - Blockchain txs
- `websocket_connections_active` - Active WS connections

### Grafana

Access: `http://localhost:3000`
Default credentials: `admin / admin`

Import dashboards:
1. Login to Grafana
2. Go to Dashboards → Import
3. Upload JSON from `monitoring/grafana/dashboards/`

---

## 🧪 Testing

### Run Tests

```bash
cd ai-service

# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::TestAuth::test_login_success -v
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host=http://localhost:5000
```

---

## 🔄 Database Migrations

### Using Alembic

```bash
cd ai-service

# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View history
alembic history
```

---

## 📦 Backup & Restore

### Database Backup

```bash
# Backup SQLite database
docker-compose exec backend sqlite3 /data/verity_ai.db ".backup '/data/backup.db'"

# Copy to host
docker cp verity-ai-backend:/data/backup.db ./backups/

# Automated backup script
./scripts/backup.sh
```

### Restore

```bash
# Copy backup to container
docker cp ./backups/backup.db verity-ai-backend:/data/

# Restore
docker-compose exec backend sqlite3 /data/verity_ai.db ".restore '/data/backup.db'"
```

---

## 🚨 Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Missing .env file
# 2. Invalid Google credentials
# 3. Port already in use

# Fix port conflict
docker-compose down
sudo lsof -i :5000
kill -9 <PID>
```

### Blockchain connection failed

```bash
# Check Ganache is running
docker-compose ps ganache

# Test connection
curl http://localhost:8545

# Restart Ganache
docker-compose restart ganache
```

### WebSocket not connecting

```bash
# Check nginx WebSocket config
# Ensure proxy_set_header Upgrade is set

# Test WebSocket
wscat -c ws://localhost:5000/api/ws?token=YOUR_JWT
```

---

## 🔒 Security Checklist

- [ ] Change default JWT_SECRET
- [ ] Use strong passwords
- [ ] Enable HTTPS in production
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable Sentry error tracking
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] API key rotation
- [ ] Database encryption at rest

---

## 📈 Performance Optimization

### Backend

```python
# Enable Redis caching
ENABLE_REDIS=true

# Increase workers
uvicorn main:app --workers 4

# Use Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Database

```bash
# SQLite optimizations
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=10000;
```

### Frontend

```bash
# Build with optimizations
npm run build

# Enable gzip in nginx (already configured)
```

---

## 📞 Support

- **Documentation**: [docs.verity-ai.com](https://docs.verity-ai.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/verity-ai/issues)
- **Email**: support@verity-ai.com

---

## 📝 License

MIT © Verity AI 2024
