from database import SessionLocal
from models import ContentDB

db = SessionLocal()
count = db.query(ContentDB).count()
print(f"DATABASE CONTENT COUNT: {count}")
db.close()
