from database import engine, Base, seed_data, SessionLocal
from models import ContentDB, InteractionDB

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("Seeding new data...")
db = SessionLocal()
# We need to manually call seed_data, but first let's make sure the check inside seed_data doesn't stop us if we just created empty tables.
# Actually seed_data checks 'if first() return'. Since we dropped tables, it is empty.
seed_data(db)

count = db.query(ContentDB).count()
print(f"DONE. Content count: {count}")
db.close()
