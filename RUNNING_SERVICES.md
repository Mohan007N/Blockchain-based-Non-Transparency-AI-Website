# Verity AI - Running Services

## ✅ Services Status

### Backend (Python FastAPI)
- **Status**: ✅ Running
- **URL**: http://localhost:5000
- **Port**: 5000
- **Process ID**: Terminal 3
- **File**: `ai-service/main_with_auth.py`
- **Features**:
  - Authentication (Register/Login)
  - Loan Application with OCR
  - Manager Approval System
  - SQLite Database
  - Zero-Knowledge Proof
  - Blockchain Hashing

### Frontend (React + Vite)
- **Status**: ✅ Running
- **URL**: http://localhost:8080
- **Port**: 8080
- **Process ID**: Terminal 4
- **Folder**: `verity-ai-main`
- **Features**:
  - Modern Landing Page
  - Professional Auth Page
  - Client Dashboard
  - Manager Dashboard
  - Real-time Updates

---

## 🗑️ Cleaned Up Files

### Removed Folders:
- ✅ `backend/` - Old Node.js backend (replaced by Python FastAPI)
- ✅ `monitoring/` - Prometheus/Grafana (not currently used)
- ✅ `scripts/` - Deployment scripts (not needed)
- ✅ `ai-service/contracts/` - Solidity contracts (not used)
- ✅ `ai-service/venv/` - Old virtual environment
- ✅ `ai-service/__pycache__/` - Python cache files

### Removed Files:
- ✅ `docker-compose.yml` - Docker setup (running directly)
- ✅ `Verity_AI.postman_collection.json` - API collection
- ✅ `ai-service/main_simple.py` - Simplified version
- ✅ `ai-service/Dockerfile` - Docker config

---

## 📁 Current Project Structure

```
verity-ai-main-main/
├── ai-service/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── blockchain/           # Blockchain hashing
│   │   ├── config/               # Database & settings
│   │   ├── decision/             # Rule engine
│   │   ├── ocr/                  # Document verification
│   │   ├── parser/               # Field parsing
│   │   ├── realtime/             # WebSocket
│   │   ├── routers/              # API routes
│   │   └── services/             # Business logic
│   ├── tests/                    # Test files
│   ├── uploads/                  # Uploaded documents
│   ├── main_with_auth.py         # ✅ Main entry point
│   ├── main.py                   # Alternative entry
│   ├── standalone_auth.py        # Auth router
│   ├── standalone_loan.py        # Loan router
│   ├── standalone_manager.py     # Manager router
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   └── verity_ai.db             # SQLite database
│
├── verity-ai-main/               # React Frontend
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── routes/              # Pages
│   │   │   ├── index.tsx        # Landing page
│   │   │   ├── auth.tsx         # Auth page
│   │   │   ├── dashboard.tsx    # Dashboard layout
│   │   │   └── dashboard.index.tsx  # Dashboard content
│   │   └── styles.css           # Global styles
│   ├── package.json             # Node dependencies
│   └── vite.config.ts           # Vite config
│
└── Documentation/
    ├── COMPLETE_IMPLEMENTATION.md
    ├── FRONTEND_IMPROVEMENTS_COMPLETE.md
    ├── MANAGER_DASHBOARD_IMPROVEMENTS.md
    └── RUNNING_SERVICES.md (this file)
```

---

## 🚀 How to Access

### 1. Landing Page
- **URL**: http://localhost:8080
- **Features**: 
  - Modern hero section
  - Feature showcase
  - How it works
  - Call-to-action

### 2. Authentication
- **URL**: http://localhost:8080/auth
- **Features**:
  - Login
  - Register
  - Google OAuth (ready for client ID)
  - Role selection (Client/Manager)

### 3. Client Dashboard
- **URL**: http://localhost:8080/dashboard
- **Login as**: Client role
- **Features**:
  - Apply for loan
  - Upload income certificate
  - Track application status
  - View verification results

### 4. Manager Dashboard
- **URL**: http://localhost:8080/dashboard
- **Login as**: Manager role
- **Features**:
  - Statistics overview
  - View all applications
  - Filter by status (All/Pending/Approved/Rejected)
  - Approve/Reject applications
  - Add comments

### 5. API Documentation
- **URL**: http://localhost:5000/api/docs
- **Features**: Interactive Swagger UI

---

## 🧪 Test Accounts

### Client Account
```
Email: test@example.com
Password: Test123!
Role: client
```

### Manager Account
```
Email: manager@example.com
Password: Manager123!
Role: manager
```

Or create new accounts via the registration page!

---

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Loan Application
- `POST /api/loans/apply` - Submit loan application
- `GET /api/loans/applications` - Get user's applications

### Manager
- `GET /api/manager/all` - Get all applications
- `GET /api/manager/pending` - Get pending applications
- `GET /api/manager/stats` - Get statistics
- `POST /api/manager/approve` - Approve/reject application

### Health
- `GET /api/health` - Health check
- `GET /` - API info

---

## 🛠️ Development Commands

### Backend
```bash
cd verity-ai-main-main/ai-service
python main_with_auth.py
```

### Frontend
```bash
cd verity-ai-main-main/verity-ai-main
npm run dev
```

### Stop Services
- Backend: Ctrl+C in terminal or stop process
- Frontend: Ctrl+C in terminal or stop process

---

## 📊 Features Implemented

### Security
- ✅ JWT Authentication
- ✅ Password hashing (bcrypt)
- ✅ Zero-knowledge proof (salary never stored)
- ✅ Blockchain hashing for immutability
- ✅ CORS enabled

### OCR & Verification
- ✅ Document upload (PDF/JPEG/PNG)
- ✅ OCR extraction (Tesseract)
- ✅ Salary verification
- ✅ Eligibility calculation
- ✅ Loan type multipliers:
  - Personal: 5x salary
  - Home: 60x salary
  - Auto: 10x salary
  - Business: 8x salary
  - Education: 12x salary

### Database
- ✅ SQLite with async support
- ✅ User management
- ✅ Application tracking
- ✅ Status management

### UI/UX
- ✅ Modern, professional design
- ✅ Gradient backgrounds
- ✅ Smooth animations
- ✅ Responsive layout
- ✅ Loading states
- ✅ Empty states
- ✅ Error handling
- ✅ Toast notifications

---

## 🎯 Next Steps

1. **Test the Application**:
   - Register as client
   - Apply for loan
   - Register as manager
   - Approve/reject applications

2. **Add Google OAuth**:
   - Get Google Client ID
   - Update frontend auth.tsx
   - Configure backend

3. **Deploy** (Optional):
   - Set up production server
   - Configure domain
   - Enable HTTPS
   - Set up monitoring

4. **Enhancements** (Optional):
   - Add more loan types
   - Improve OCR accuracy
   - Add email notifications
   - Add analytics dashboard
   - Add export functionality

---

## 📝 Notes

- Database file: `ai-service/verity_ai.db`
- Uploaded documents: `ai-service/uploads/`
- Environment variables: `ai-service/.env`
- Frontend runs on port 8080
- Backend runs on port 5000
- Both services support hot reload

---

**Status**: ✅ All Services Running
**Date**: 2026-04-29
**Ready for**: Testing and Development
