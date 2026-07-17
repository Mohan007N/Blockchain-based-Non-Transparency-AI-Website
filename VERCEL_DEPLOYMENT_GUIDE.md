# Vercel Deployment Guide - Verity AI

This guide covers deploying the Verity AI React frontend to Vercel while maintaining connection to your FastAPI backend.

## 📋 Prerequisites

- Vercel account (https://vercel.com)
- GitHub repository connected to Vercel
- FastAPI backend deployed (on a separate service)
- Environment variables configured

## 🚀 Quick Start

### 1. Connect to Vercel

```bash
# Option A: CLI
npm install -g vercel
vercel login
cd web
vercel

# Option B: Via GitHub
# 1. Go to https://vercel.com/new
# 2. Import your GitHub repository
# 3. Select root directory: `web`
# 4. Click Deploy
```

### 2. Configure Environment Variables

#### In Vercel Dashboard:

1. Go to Settings → Environment Variables
2. Add the following:

```
VITE_API_URL=https://your-backend-api.com
# or if backend is on same domain:
VITE_API_URL=/api
```

#### Update your frontend code to use this:

In `web/src/` files, replace hardcoded API URLs with:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Usage
const response = await fetch(`${API_URL}/api/verify-document`, {
  method: 'POST',
  body: formData,
});
```

### 3. Backend API Configuration

#### Option A: Backend on Separate Domain

If your backend is deployed at `https://api.yourdomain.com`:

```bash
# In Vercel Environment Variables
VITE_API_URL=https://api.yourdomain.com
```

Update `web/vite.config.ts`:
```typescript
export default defineConfig({
  vite: {
    server: {
      proxy: {
        '/api': {
          target: process.env.VITE_API_URL || 'http://localhost:5000',
          changeOrigin: true,
          secure: false,
        },
      },
    },
  },
});
```

#### Option B: Backend on Same Domain (Recommended)

If using Nginx to proxy backend:

```nginx
# Nginx configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # Frontend (Vercel)
    location / {
        proxy_pass https://your-project.vercel.app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 4. Update CORS Settings

In your FastAPI backend (`ai-service/main.py`), configure CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-project.vercel.app",
        "https://yourdomain.com",
        "http://localhost:3000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Update Web Package.json

Ensure your `web/package.json` includes:

```json
{
  "name": "verity-ai-frontend",
  "type": "module",
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## 🔐 Security Configuration

### 1. HTTPS Enforcement

Add to `web/src/lib/api.ts`:

```typescript
// Enforce HTTPS in production
if (typeof window !== 'undefined' && window.location.protocol === 'http:') {
  if (process.env.NODE_ENV === 'production') {
    window.location.protocol = 'https:';
  }
}
```

### 2. API Key Management

Never commit `.env` files. Use Vercel's environment variable dashboard:

```bash
# .env.local (local development only)
VITE_API_URL=http://localhost:5000

# .env.production
VITE_API_URL=https://api.yourdomain.com
```

### 3. Content Security Policy

Add headers in `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

## 🧪 Testing Before Deploy

### Local Testing

```bash
cd web

# Development
npm run dev
# Access at http://localhost:5173

# Production build preview
npm run build
npm run preview
```

### Test API Connectivity

```bash
# Test health check
curl https://your-backend.com/api/health

# Test with frontend
# Open DevTools → Network tab
# Make a request to verify /api calls work
```

## 📊 Monitoring

### Vercel Analytics

1. Go to Vercel Dashboard → Project Settings → Analytics
2. Enable Web Vitals
3. Monitor performance metrics

### Backend Health Checks

Add to your FastAPI backend:

```python
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

Add in Vercel project settings → Deployments → Health checks:
- URL: `https://api.yourdomain.com/api/health`
- Interval: 60s

## 🔄 CI/CD Pipeline

### GitHub Actions Integration

Create `.github/workflows/vercel-deploy.yml`:

```yaml
name: Vercel Deploy

on:
  push:
    branches: [main, develop]
    paths:
      - 'web/**'
      - '.github/workflows/vercel-deploy.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: web
```

Get these values:
```bash
cd web
vercel link  # Get org and project IDs
vercel env pull .env.local
# Store VERCEL_TOKEN from https://vercel.com/account/tokens
```

## 🚨 Troubleshooting

### Build Fails

```bash
# Check Node version
node --version  # Should be 18+

# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check build
npm run build
```

### API Calls 404

1. Verify `VITE_API_URL` is set correctly in Vercel dashboard
2. Check backend is accessible: `curl $VITE_API_URL/api/health`
3. Verify CORS is configured on backend
4. Check browser DevTools → Network tab for actual URLs

### WebSocket Connection Failed

Add to Nginx configuration:

```nginx
location /api/ws {
    proxy_pass http://backend:5000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Slow Performance

1. Check Vercel Analytics for bottlenecks
2. Enable gzip compression on backend
3. Use CDN for static assets
4. Optimize images in React components

## 📚 Additional Resources

- [Vercel Docs](https://vercel.com/docs)
- [TanStack Start Deployment](https://tanstack.com/start/latest/docs/deployment)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

## ✅ Deployment Checklist

- [ ] Frontend builds successfully locally
- [ ] Environment variables set in Vercel
- [ ] Backend API URL configured
- [ ] CORS enabled on backend
- [ ] SSL/HTTPS enabled
- [ ] API health check passing
- [ ] Test login workflow
- [ ] Test file upload
- [ ] Monitor error tracking
- [ ] Setup backup strategy

## 🎯 Next Steps

1. **Deploy Frontend**: Push to GitHub and watch Vercel auto-deploy
2. **Deploy Backend**: Use Docker on separate service (AWS, Digital Ocean, Railway, etc.)
3. **Setup Monitoring**: Configure Sentry for error tracking
4. **Enable Analytics**: Monitor performance in Vercel dashboard
5. **Setup Backups**: Implement automated database backups

---

For production deployment questions, refer to `DEPLOYMENT.md` for backend setup.
