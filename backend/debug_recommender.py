from database import SessionLocal, seed_data, engine, Base
from models import ContentDB, InteractionDB
from recommender import RecommenderEngine
import random

# Init DB
Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_data(db)

# Create a fake user
user_id = f"debug_user_{random.randint(1000,9999)}"
print(f"--- Debugging User: {user_id} ---")

# 1. Initial State (Cold Start)
rec_engine = RecommenderEngine(db)
initial_recs = rec_engine.get_recommendations(user_id)
print(f"\n[1] Initial Recommendations (Expected Random):")
for item in initial_recs:
    print(f"   - {item.title} ({item.category})")

# 2. Simulate Like on a Basketball item
# Find a basketball item
basketball_item = db.query(ContentDB).filter(ContentDB.category == "Basketball").first()
print(f"\n[2] User LIKES: {basketball_item.title} (ID: {basketball_item.id})")

interaction = InteractionDB(user_id=user_id, content_id=basketball_item.id, interaction_type="like")
db.add(interaction)
db.commit()

# 3. Get Recommendations Again
context_recs = rec_engine.get_recommendations(user_id)
print(f"\n[3] Post-Like Recommendations (Expected Basketball focus, WITHOUT the liked item):")
for item in context_recs:
    print(f"   - {item.title} ({item.category}) [ID: {item.id}]")
    if item.id == basketball_item.id:
        print("   !!! ERROR: Liked item is still in recommendations!")

# 4. Like another Basketball item from the list
if context_recs:
    next_item = context_recs[0]
    print(f"\n[4] User LIKES Recommended: {next_item.title} (ID: {next_item.id})")
    interaction2 = InteractionDB(user_id=user_id, content_id=next_item.id, interaction_type="like")
    db.add(interaction2)
    db.commit()
    
    final_recs = rec_engine.get_recommendations(user_id)
    print(f"\n[5] Final Recommendations:")
    for item in final_recs:
        print(f"   - {item.title} ({item.category}) [ID: {item.id}]")
        if item.id in [basketball_item.id, next_item.id]:
            print("   !!! ERROR: Liked item is still in system!")

db.close()
