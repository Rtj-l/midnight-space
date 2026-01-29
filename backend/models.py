from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
from pydantic import BaseModel
from typing import List, Optional

# --- SQLAlchemy Models (Database) ---

class ContentDB(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True) # e.g., Basketball, Football, eSports
    content_type = Column(String, default="video") # video, article, ticket, merchandise
    tags = Column(String) # Comma-separated tags
    image_url = Column(String)
    action_url = Column(String) # URL to video/shop/ticket
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class InteractionDB(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    content_id = Column(Integer, ForeignKey("content.id"))
    interaction_type = Column(String) # 'like', 'view'
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    content = relationship("ContentDB")

# --- Pydantic Models (API) ---

class ContentBase(BaseModel):
    title: str
    category: str
    content_type: str = "video"
    tags: str
    image_url: str
    action_url: str

class ContentCreate(ContentBase):
    pass

class Content(ContentBase):
    id: int
    
    class Config:
        orm_mode = True

class InteractionCreate(BaseModel):
    user_id: str
    content_id: int
    interaction_type: str = "like"

class UserProfile(BaseModel):
    user_id: str
    top_interests: List[str]

