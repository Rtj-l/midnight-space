from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import engine, Base, get_db, seed_data
import models
from recommender import RecommenderEngine
import os

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cyberpunk Sports Recommender API")

# Serve Static Files (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB with Seed Data
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    seed_data(db)

@app.get("/")
def read_root():
    return FileResponse('static/index.html')

@app.get("/content", response_model=list[models.Content])
def get_all_content(db: Session = Depends(get_db)):
    """Get all content items library."""
    return db.query(models.ContentDB).all()

@app.get("/recommend/{user_id}", response_model=list[models.Content])
def get_recommendations(user_id: str, db: Session = Depends(get_db)):
    """Get personalized recommendations for a user."""
    engine = RecommenderEngine(db)
    return engine.get_recommendations(user_id)

@app.post("/interact")
def record_interaction(interaction: models.InteractionCreate, db: Session = Depends(get_db)):
    """Record a user interaction (Like)."""
    db_interaction = models.InteractionDB(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    return {"status": "recorded", "user_id": interaction.user_id, "content_id": interaction.content_id}

@app.get("/profile/{user_id}")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Debug endpoint to see what the system thinks the user likes."""
    interactions = db.query(models.InteractionDB).filter(models.InteractionDB.user_id == user_id).all()
    categories = {}
    for i in interactions:
        cat = i.content.category
        categories[cat] = categories.get(cat, 0) + 1
    return {"user_id": user_id, "interaction_count": len(interactions), "category_preference": categories}
