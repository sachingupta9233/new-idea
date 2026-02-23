# 🚀 Render Deployment Guide

Navi Mumbai House Price Predictor is now ready to deploy on Render (free tier compatible)!

---

## 📋 Prerequisites

✅ GitHub account with the project pushed  
✅ Render.com account (free tier)  
✅ Project files in root: `requirements.txt`, `Procfile`, `start.py`

---

## 🎯 Quick Setup (5 minutes)

### Step 1: Push to GitHub
```bash
cd /Users/sachingupta/Desktop/house
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Create Render Service

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `navi-mumbai-predictor`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start.py`
   - **Plan**: Free
   - **Environment**: Python 3.11

### Step 3: Set Environment Variables

Click **"Environment"** and add:

```
DEBUG=false
DATABASE_URL=sqlite:///./navi_mumbai_house.db
SECRET_KEY=your-secure-secret-key-here
```

### Step 4: Deploy

Click **"Create Web Service"** and wait 3-5 minutes.

**Your API will be live at**: `https://navi-mumbai-predictor.onrender.com`

---

## 📡 API Endpoints

Once deployed, access:

- **API Base**: `https://navi-mumbai-predictor.onrender.com/api/v1`
- **API Docs**: `https://navi-mumbai-predictor.onrender.com/docs`
- **Health Check**: `https://navi-mumbai-predictor.onrender.com/health`

### Example: Get Price Prediction

```bash
curl -X POST https://navi-mumbai-predictor.onrender.com/api/v1/prediction/predict \
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

---

## 📱 Deploying Frontend (React)

### Option A: As Part of Same Service (Recommended)

1. Update `frontend/.env`:
```
REACT_APP_API_URL=https://navi-mumbai-predictor.onrender.com/api/v1
```

2. Update `Procfile` to serve both:
```
web: python start.py
```

### Option B: Separate Frontend Service

1. Create new Render service from `frontend/` directory
2. Build command: `npm install && npm run build`
3. Static site from: `build`

---

## 🔧 Configuration Files Explained

### `requirements.txt` (Root)
Contains all Python dependencies needed by Render

### `Procfile`
Tells Render how to start the application:
```
web: python start.py
```

### `start.py`
Main startup script that:
- Initializes the SQLite database
- Seeds 14 localities
- Starts the FastAPI server

### `render.yaml` (Optional)
Advanced configuration for multi-service deployments

---

## ✅ Deployment Checklist

- [ ] Project pushed to GitHub
- [ ] `requirements.txt` in root directory
- [ ] `Procfile` configured
- [ ] `start.py` exists
- [ ] Models trained (`models/*.pkl` files)
- [ ] Environment variables set on Render
- [ ] Free tier selected (no credit card required)
- [ ] Deployment triggered

---

## 🆘 Troubleshooting

### Error: "No such file or directory: 'requirements.txt'"
**Solution**: Ensure `requirements.txt` is in the **root** directory, not in `backend/`

### Error: "ModuleNotFoundError: No module named 'main'"
**Solution**: Update start command to include proper path:
```
python start.py
```

### Database Not Initializing
**Solution**: Check Render logs and ensure `start.py` has execute permissions:
```bash
chmod +x /Users/sachingupta/Desktop/house/start.py
```

### API Too Slow
**Solution**: Render free tier is slower. Consider upgrading to Starter tier for better performance.

---

## 📊 Render Free Tier Limits

| Resource | Limit |
|----------|-------|
| Web Services | 1 at a time |
| Memory | 0.5 GB |
| CPU | Shared |
| Storage | Ephemeral (resets on redeploy) |
| Build Time | 30 mins |
| Inactivity Auto-Spin Down | Yes (15 mins) |

**Note**: Use persistent database (PostgreSQL) for production data

---

## 🚀 Production Considerations

### For Better Performance

1. **Upgrade Plan**: Use Starter tier ($7/month)
2. **Database**: Connect to Render PostgreSQL instead of SQLite
3. **Caching**: Enable Redis for API caching
4. **Workers**: Increase gunicorn workers to 4+

### Configuration for Production

```yaml
# Update environment if upgrading
DATABASE_URL=postgresql://user:pass@db.onrender.com:5432/navi_mumbai
REDIS_URL=redis://cache:6379
DEBUG=false
```

---

## 📞 Next Steps

1. **Immediate**: Deploy backend to Render (this guide)
2. **Week 2**: Deploy frontend as separate service
3. **Week 3**: Set up PostgreSQL database
4. **Week 4**: Configure custom domain

---

## 📚 Resources

- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Project API Docs](./docs/API_REFERENCE.md)
- [Full README](./README.md)

---

**Status**: Ready to Deploy ✅  
**Estimated Time**: 5 minutes  
**Free Tier**: Yes 🎉  
**Production Ready**: With optimizations
