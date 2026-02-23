# 🔧 Command Reference - Navi Mumbai House Price Predictor

## 🚀 Quick Start Commands

### Start Everything with Docker (Recommended)
```bash
cd /Users/sachingupta/Desktop/house
docker-compose up --build
```

**Then access:**
- Frontend: http://localhost:3000 ✓
- API: http://localhost:8000 ✓
- Swagger Docs: http://localhost:8000/docs ✓

---

## 🖥️ Local Development Commands

### Setup Backend
```bash
cd /Users/sachingupta/Desktop/house/backend

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates tables and 14 localities)
python init_db.py

# Train ML model (already done, but you can retrain)
cd ..
python train_model.py

# Start API server
cd backend
uvicorn main:app --reload --port 8000
```

### Setup Frontend
```bash
cd /Users/sachingupta/Desktop/house/frontend

# Install dependencies
npm install

# Start development server
npm start
# Opens http://localhost:3000
```

---

## 🧪 Testing & Debugging

### Test API with curl

#### Get Price Prediction
```bash
curl -X POST http://localhost:8000/api/v1/prediction/predict \
  -H "Content-Type: application/json" \
  -d '{
    "locality_name": "Vashi",
    "bhk": 2,
    "carpet_area_sqft": 1200,
    "floor_number": 8,
    "total_floors": 15,
    "building_age_years": 5,
    "lift": true,
    "parking": true,
    "gym": true,
    "swimming_pool": false,
    "gated_society": true,
    "cctv": true
  }'
```

#### Get All Localities
```bash
curl http://localhost:8000/api/v1/localities/
```

#### Get 6-Month Price Trend
```bash
curl http://localhost:8000/api/v1/trends/Vashi/6m
```

#### Get Comparable Properties
```bash
curl http://localhost:8000/api/v1/properties/locality/2?limit=10
```

#### Health Check
```bash
curl http://localhost:8000/health
```

---

## 🗄️ Database Commands

### Reset Database
```bash
cd /Users/sachingupta/Desktop/house/backend
python init_db.py
```

### Connect to Database (if running locally)
```bash
psql -U postgres -h localhost -d navi_mumbai_house
```

### View Database in Docker
```bash
docker exec -it navi_mumbai_db psql -U postgres -d navi_mumbai_house
```

---

## 📊 ML Model Commands

### Train New Model
```bash
cd /Users/sachingupta/Desktop/house
python train_model.py
```

### Train with Custom Data (if you have CSV)
```python
cd /Users/sachingupta/Desktop/house
python3 << 'EOF'
from ml.model_trainer import ModelTrainer
trainer = ModelTrainer()
metrics = trainer.train(df=your_dataframe)
trainer.save_model()
EOF
```

---

## 🐳 Docker Commands

### Build Images
```bash
cd /Users/sachingupta/Desktop/house
docker-compose build
```

### Start Services
```bash
docker-compose up
```

### Start in Background
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f backend      # Backend logs
docker-compose logs -f frontend     # Frontend logs
docker-compose logs -f db           # Database logs
docker-compose logs -f redis        # Redis logs
```

### Stop All Services
```bash
docker-compose down
```

### Stop & Remove Data
```bash
docker-compose down -v
```

### Restart Specific Service
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Execute Command in Container
```bash
docker-compose exec backend python init_db.py
docker-compose exec db psql -U postgres -d navi_mumbai_house
```

---

## 🎯 Common Development Tasks

### Reinstall Python Dependencies
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Reinstall Frontend Dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Fix Port Conflicts
```bash
# Port 8000 (Backend)
lsof -i :8000
kill -9 <PID>

# Port 3000 (Frontend)
lsof -i :3000
kill -9 <PID>

# Port 5432 (Database)
lsof -i :5432
kill -9 <PID>

# Port 6379 (Redis)
lsof -i :6379
kill -9 <PID>
```

### Check Services Status
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000 2>&1 | head -5

# Database
psql -U postgres -h localhost -c "SELECT 1"

# Redis
redis-cli ping
```

---

## 📝 File Editing Commands

### Edit Configuration
```bash
# Development
nano /Users/sachingupta/Desktop/house/.env

# Docker
nano /Users/sachingupta/Desktop/house/docker-compose.yml
```

### Add New API Endpoint
1. Create file in `backend/routers/`
2. Define router: `router = APIRouter()`
3. Add endpoint: `@router.get/post(...)`
4. Include in `backend/main.py`: `app.include_router(...)`

### Add New Database Table
1. Create model in `backend/models.py`
2. Add schema in `backend/schemas.py`
3. Run: `python backend/init_db.py`

---

## 🔍 Debugging Commands

### Check Python Version
```bash
python3 --version
```

### Check Node Version
```bash
node --version
npm --version
```

### Check PostgreSQL
```bash
psql --version
```

### View Project Structure
```bash
tree -L 2 /Users/sachingupta/Desktop/house
```

### Count Lines of Code
```bash
find /Users/sachingupta/Desktop/house -type f \( -name "*.py" -o -name "*.jsx" -o -name "*.json" \) | xargs wc -l | tail -1
```

### List All API Endpoints
```bash
cd /Users/sachingupta/Desktop/house/backend
grep -r "@router" routers/
```

---

## 📦 Deployment Commands

### Build Production Docker Image
```bash
docker build -t navi-mumbai-predictor:latest .
```

### Export Docker Image
```bash
docker save navi-mumbai-predictor:latest > navi-mumbai-predictor.tar
```

### Test Production Build Locally
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/navi_mumbai_house \
  navi-mumbai-predictor:latest
```

---

## 🧹 Cleanup Commands

### Clean Python Cache
```bash
find /Users/sachingupta/Desktop/house -type d -name __pycache__ -exec rm -rf {} +
find /Users/sachingupta/Desktop/house -type f -name "*.pyc" -delete
```

### Clean Node Modules
```bash
cd /Users/sachingupta/Desktop/house/frontend
rm -rf node_modules package-lock.json
npm install
```

### Clean Docker
```bash
docker system prune -a          # Remove unused images
docker volume prune             # Remove unused volumes
docker-compose down -v          # Remove volumes created by docker-compose
```

---

## 📚 Documentation Commands

### Open README
```bash
cat /Users/sachingupta/Desktop/house/README.md | less
```

### Open API Reference
```bash
cat /Users/sachingupta/Desktop/house/docs/API_REFERENCE.md | less
```

### Generate API Docs
Visit: http://localhost:8000/docs (auto-generated by FastAPI)

---

## 🎓 Learning Commands

### View Model Performance
```bash
python3 << 'EOF'
from ml.model_trainer import ModelTrainer
trainer = ModelTrainer()
trainer.load_model()
print("Model loaded successfully!")
print(f"Features: {trainer.feature_names}")
EOF
```

### Test Prediction Service
```bash
cd /Users/sachingupta/Desktop/house/backend
python3 << 'EOF'
from services.prediction_service import PredictionService
from database import SessionLocal

db = SessionLocal()
service = PredictionService(db)
print("Prediction service ready!")
EOF
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas numpy scikit-learn xgboost joblib
```

### "Connection refused" (Database)
```bash
# Start PostgreSQL if not running
brew services start postgresql

# Or use Docker
docker-compose up db
```

### "XGBoostError: Library (libxgboost.dylib) could not be loaded" (macOS)
```bash
brew install libomp
pip install --upgrade xgboost
```

### "Port already in use"
```bash
# Kill the process using the port
lsof -i :<PORT>
kill -9 <PID>
```

### "npm ERR! EACCES: permission denied"
```bash
npm install --force
# Or use sudo (not recommended)
sudo npm install
```

---

**Last Updated**: February 23, 2026  
**Location**: /Users/sachingupta/Desktop/house  
**Status**: Ready to Use ✅
