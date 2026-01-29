from sqlalchemy.orm import Session
from models import ContentDB, InteractionDB
from sqlalchemy import func
import random

class RecommenderEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_recommendations(self, user_id: str, limit: int = 5):
        # 1. Get user interactions
        interactions = self.db.query(InteractionDB).filter(InteractionDB.user_id == user_id).all()
        
        # 2. Build User Profile (Primitive Tag Weighting)
        tag_scores = {}
        category_scores = {}
        
        if not interactions:
            # Cold Start: Return trending or random content
            # For MVP, just return random
            return self.db.query(ContentDB).order_by(func.random()).limit(limit).all()

        for interaction in interactions:
            content = interaction.content
            # Weighting: Like = 1 
            weight = 1 
            
            # Category score
            category_scores[content.category] = category_scores.get(content.category, 0) + weight
            
            # Tag score
            for tag in content.tags.split(','):
                tag = tag.strip()
                tag_scores[tag] = tag_scores.get(tag, 0) + weight

        # 3. Score all content candidates
        # Determine top categories
        top_categories = sorted(category_scores, key=category_scores.get, reverse=True)[:2]
        
        # 4. Score all content candidates
        all_content = self.db.query(ContentDB).all()
        scored_content = []
        
        interacted_ids = {i.content_id for i in interactions}

        for item in all_content:
            if item.id in interacted_ids:
                continue # Don't recommend what's already seen/liked
            
            score = 0
            # Boost for Category Match
            if item.category in top_categories:
                score += 5  # Higher weight
            
            # Boost for Tag Match
            for tag in item.tags.split(','):
                if tag.strip() in tag_scores:
                    score += tag_scores[tag.strip()] * 0.5
            
            # Add significant randomness to shuffle items with similar scores
            score += random.random() * 2.0 
            
            scored_content.append((item, score))
            
        # 5. Sort and return
        scored_content.sort(key=lambda x: x[1], reverse=True)
        
        # VARIETY FIX: Take top 15 matches, shuffle them, and pick 4.
        # This ensures specific order changes every time user asks.
        candidates = [item[0] for item in scored_content[:15]]
        random.shuffle(candidates)
        recommendations = candidates[:4]
        
        # Add 1 Pure Discovery Item (Exploration) - Random from deep storage
        remaining = [item[0] for item in scored_content[15:]]
        if remaining:
            recommendations.append(random.choice(remaining))
            
        return recommendations
