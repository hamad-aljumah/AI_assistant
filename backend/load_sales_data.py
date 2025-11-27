import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent))

from app.database import engine, SessionLocal
from app.models.database_models import Sales, Base
from app.config import get_settings

settings = get_settings()


def load_csv_to_database(csv_path: str):
    """Load supermarket sales data from CSV into PostgreSQL database"""
    
    print(f"Loading data from: {csv_path}")
    
    # Read CSV file
    try:
        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} rows in CSV file")
        print(f"Columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified")
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Clear existing data (optional - remove if you want to keep existing data)
        existing_count = db.query(Sales).count()
        if existing_count > 0:
            response = input(f"Database has {existing_count} existing records. Delete them? (yes/no): ")
            if response.lower() == 'yes':
                db.query(Sales).delete()
                db.commit()
                print(f"Deleted {existing_count} existing records")
        
        # Process and insert data
        records_added = 0
        errors = 0
        
        for index, row in df.iterrows():
            try:
                # Parse date (handle different date formats)
                date_str = str(row['Date'])
                try:
                    date_obj = pd.to_datetime(date_str).date()
                except:
                    date_obj = datetime.strptime(date_str, '%m/%d/%Y').date()
                
                # Calculate total
                unit_price = float(row['Unit price'])
                quantity = int(row['Quantity'])
                total = unit_price * quantity
                
                # Create Sales record
                sales_record = Sales(
                    date=date_obj,
                    branch=str(row['Branch']),
                    customer_type=str(row['Customer type']),
                    gender=str(row['Gender']),
                    product_line=str(row['Product line']),
                    unit_price=unit_price,
                    quantity=quantity,
                    payment=str(row['Payment']),
                    rating=float(row['Rating']),
                    total=total
                )
                
                db.add(sales_record)
                records_added += 1
                
                # Commit in batches of 100
                if records_added % 100 == 0:
                    db.commit()
                    print(f"Processed {records_added} records...")
                    
            except Exception as e:
                errors += 1
                print(f"Error processing row {index}: {e}")
                continue
        
        # Final commit
        db.commit()
        
        print(f"\n✓ Successfully loaded {records_added} records into the database")
        if errors > 0:
            print(f"✗ {errors} records failed to load")
        
        # Verify data
        total_records = db.query(Sales).count()
        print(f"Total records in database: {total_records}")
        
    except Exception as e:
        print(f"Error during import: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Path to CSV file (relative to backend directory)
    # Try multiple possible locations
    possible_paths = [
        Path(__file__).parent / "Supermarket_Sales.csv",  # Same directory as script
        Path(__file__).parent.parent / "Supermarket_Sales.csv",  # Local development
        Path("/app") / "Supermarket_Sales.csv",  # Docker root
    ]
    
    csv_path = None
    for path in possible_paths:
        if path.exists():
            csv_path = path
            break
    
    if csv_path is None:
        print(f"Error: CSV file not found in any of these locations:")
        for path in possible_paths:
            print(f"  - {path}")
        print("\nPlease ensure Supermarket_Sales.csv is in the project root directory")
        sys.exit(1)
    
    load_csv_to_database(str(csv_path))
