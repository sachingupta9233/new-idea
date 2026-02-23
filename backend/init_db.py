"""
Database initialization and migration utilities
"""

from sqlalchemy import inspect
from database import engine, SessionLocal, Base
from models import Locality, Property, User, Prediction, SavedEstimate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database and create all tables"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialization complete!")


def seed_localities():
    """Seed initial locality data"""
    db = SessionLocal()
    
    localities_data = [
        {
            "name": "Kharghar",
            "node_type": "Residential",
            "metro_distance_km": 8.5,
            "highway_distance_km": 2.0,
            "avg_price_per_sqft": 85000
        },
        {
            "name": "Vashi",
            "node_type": "Mixed",
            "metro_distance_km": 0.5,
            "highway_distance_km": 3.0,
            "avg_price_per_sqft": 120000
        },
        {
            "name": "Panvel",
            "node_type": "Residential",
            "metro_distance_km": 15.0,
            "highway_distance_km": 5.0,
            "avg_price_per_sqft": 65000
        },
        {
            "name": "Nerul",
            "node_type": "CBD",
            "metro_distance_km": 2.0,
            "highway_distance_km": 4.0,
            "avg_price_per_sqft": 110000
        },
        {
            "name": "Belapur",
            "node_type": "CBD",
            "metro_distance_km": 3.0,
            "highway_distance_km": 5.0,
            "avg_price_per_sqft": 105000
        },
        {
            "name": "Airoli",
            "node_type": "Residential",
            "metro_distance_km": 7.0,
            "highway_distance_km": 2.5,
            "avg_price_per_sqft": 95000
        },
        {
            "name": "Ulwe",
            "node_type": "Emerging",
            "metro_distance_km": 18.0,
            "highway_distance_km": 6.0,
            "avg_price_per_sqft": 55000
        },
        {
            "name": "Dronagiri",
            "node_type": "Emerging",
            "metro_distance_km": 20.0,
            "highway_distance_km": 7.0,
            "avg_price_per_sqft": 50000
        },
        {
            "name": "CBD Belapur",
            "node_type": "CBD",
            "metro_distance_km": 1.0,
            "highway_distance_km": 4.5,
            "avg_price_per_sqft": 130000
        },
        {
            "name": "Seawoods",
            "node_type": "Premium",
            "metro_distance_km": 5.0,
            "highway_distance_km": 6.0,
            "avg_price_per_sqft": 150000
        },
        {
            "name": "Koparkhairane",
            "node_type": "Residential",
            "metro_distance_km": 6.0,
            "highway_distance_km": 3.5,
            "avg_price_per_sqft": 100000
        },
        {
            "name": "Ghansoli",
            "node_type": "Residential",
            "metro_distance_km": 12.0,
            "highway_distance_km": 4.0,
            "avg_price_per_sqft": 80000
        },
        {
            "name": "Kamothe",
            "node_type": "Residential",
            "metro_distance_km": 16.0,
            "highway_distance_km": 5.5,
            "avg_price_per_sqft": 70000
        },
        {
            "name": "Taloje",
            "node_type": "Industrial",
            "metro_distance_km": 20.0,
            "highway_distance_km": 2.0,
            "avg_price_per_sqft": 45000
        }
    ]
    
    try:
        for loc_data in localities_data:
            # Check if locality already exists
            existing = db.query(Locality).filter(
                Locality.name == loc_data["name"]
            ).first()
            
            if not existing:
                locality = Locality(**loc_data)
                db.add(locality)
                logger.info(f"Added locality: {loc_data['name']}")
            else:
                logger.info(f"Locality {loc_data['name']} already exists")
        
        db.commit()
        logger.info("Locality seeding complete!")
    except Exception as e:
        logger.error(f"Error seeding localities: {e}")
        db.rollback()
    finally:
        db.close()


def check_db_status():
    """Check database connectivity and table status"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Database connected. Tables: {tables}")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


if __name__ == "__main__":
    logger.info("Starting database initialization...")
    
    # Check database
    if not check_db_status():
        logger.error("Cannot connect to database. Please check your DATABASE_URL")
        exit(1)
    
    # Initialize database
    init_db()
    
    # Seed data
    seed_localities()
    
    logger.info("Database setup complete!")
