#!/usr/bin/env python
"""
Render deployment startup script
Initializes database and starts the FastAPI application
"""

import os
import sys
import subprocess

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set up database URL (use SQLite for simplicity on free tier)
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./navi_mumbai_house.db'

# Change to backend directory
os.chdir(backend_path)

# Initialize database
print("Initializing database...")
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base, Locality
    from database import engine, SessionLocal

    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Add localities if not present
    db = SessionLocal()
    existing_count = db.query(Locality).count()
    
    if existing_count == 0:
        print("Seeding 14 localities...")
        localities_data = [
            {"name": "Kharghar", "node_type": "Residential", "metro_distance_km": 8.5, "highway_distance_km": 2.0, "avg_price_per_sqft": 85000},
            {"name": "Vashi", "node_type": "Mixed", "metro_distance_km": 0.5, "highway_distance_km": 3.0, "avg_price_per_sqft": 120000},
            {"name": "Panvel", "node_type": "Residential", "metro_distance_km": 15.0, "highway_distance_km": 5.0, "avg_price_per_sqft": 65000},
            {"name": "Nerul", "node_type": "CBD", "metro_distance_km": 2.0, "highway_distance_km": 4.0, "avg_price_per_sqft": 110000},
            {"name": "Belapur", "node_type": "CBD", "metro_distance_km": 3.0, "highway_distance_km": 5.0, "avg_price_per_sqft": 105000},
            {"name": "Airoli", "node_type": "Residential", "metro_distance_km": 7.0, "highway_distance_km": 2.5, "avg_price_per_sqft": 95000},
            {"name": "Ulwe", "node_type": "Emerging", "metro_distance_km": 18.0, "highway_distance_km": 6.0, "avg_price_per_sqft": 55000},
            {"name": "Dronagiri", "node_type": "Emerging", "metro_distance_km": 20.0, "highway_distance_km": 7.0, "avg_price_per_sqft": 50000},
            {"name": "CBD Belapur", "node_type": "CBD", "metro_distance_km": 1.0, "highway_distance_km": 4.5, "avg_price_per_sqft": 130000},
            {"name": "Seawoods", "node_type": "Premium", "metro_distance_km": 5.0, "highway_distance_km": 6.0, "avg_price_per_sqft": 150000},
            {"name": "Koparkhairane", "node_type": "Residential", "metro_distance_km": 6.0, "highway_distance_km": 3.5, "avg_price_per_sqft": 100000},
            {"name": "Ghansoli", "node_type": "Residential", "metro_distance_km": 12.0, "highway_distance_km": 4.0, "avg_price_per_sqft": 80000},
            {"name": "Kamothe", "node_type": "Residential", "metro_distance_km": 16.0, "highway_distance_km": 5.5, "avg_price_per_sqft": 70000},
            {"name": "Taloje", "node_type": "Industrial", "metro_distance_km": 20.0, "highway_distance_km": 2.0, "avg_price_per_sqft": 45000}
        ]
        
        for loc_data in localities_data:
            locality = Locality(**loc_data)
            db.add(locality)
        
        db.commit()
        print(f"✓ Seeded {len(localities_data)} localities")
    else:
        print(f"✓ Database already has {existing_count} localities")
    
    db.close()
    print("✓ Database initialized successfully")
    
except Exception as e:
    print(f"Database initialization error: {e}")
    print("Continuing anyway...")

# Get port from environment or default to 8000
port = os.getenv('PORT', '8000')

# Start the application
print(f"\n🚀 Starting FastAPI application on port {port}...")
os.execv(sys.executable, [
    sys.executable, '-m', 'uvicorn',
    'main:app',
    '--host', '0.0.0.0',
    '--port', port
])
