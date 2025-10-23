"""Fix NULL status values in database."""
from database import SessionLocal
from models import Case

def fix_null_status():
    """Update all cases with NULL status to 'OPEN'."""
    db = SessionLocal()
    try:
        # Find cases with NULL status
        null_cases = db.query(Case).filter(Case.status == None).all()
        
        print(f"Found {len(null_cases)} cases with NULL status")
        
        # Update them to OPEN
        for case in null_cases:
            case.status = 'OPEN'
            print(f"Updated case {case.control_no} to OPEN")
        
        db.commit()
        print(f"✅ Successfully updated {len(null_cases)} cases")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_null_status()
