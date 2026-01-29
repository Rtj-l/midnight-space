from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./mvp_sports.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Seeding Data (for MVP) ---
def seed_data(db):
    from models import ContentDB
    if db.query(ContentDB).first():
        return

    # Mock Data: Futuristic Sports Theme
    # Types: video, article, ticket, merchandise, live
    initial_content = [
        # --- BASKETBALL ---
        {"title": "Neon Dunk: Cyber-League Highlights", "category": "Basketball", "content_type": "video", "tags": "dunk,highlights,cyber-league", "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ee2?w=800", "action_url": "https://www.youtube.com/embed/3e2D8c6s42Y?autoplay=1"},
        {"title": "Holo-Court Tactics: Lakers vs Robots", "category": "Basketball", "content_type": "article", "tags": "tactics,analysis,reading", "image_url": "https://images.unsplash.com/photo-1519861531473-92002639313a?w=800", "action_url": "https://www.nba.com/news"},
        {"title": "TICKET: Cyber-Finals Front Row", "category": "Basketball", "content_type": "ticket", "tags": "ticket,live,finals,vip", "image_url": "https://images.unsplash.com/photo-1504450758481-7338eba7524a?w=800", "action_url": "https://www.ticketmaster.com/nba"},
        {"title": "Jersey: LeBron 2077 Haptic Suit", "category": "Basketball", "content_type": "merchandise", "tags": "gear,shop,jersey,tech", "image_url": "https://images.unsplash.com/photo-1533290686950-8b4d817b1b01?w=800", "action_url": "https://store.nba.com/"},
        
        # --- SOCCER ---
        {"title": "Legendary Goal: 500m Kick", "category": "Soccer", "content_type": "video", "tags": "highlights,retro,legend,soccer", "image_url": "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?w=800", "action_url": "https://www.youtube.com/embed/m1k5t4t8s8w?autoplay=1"},
        {"title": "Zero-G Soccer Final", "category": "Soccer", "content_type": "video", "tags": "goal,final,zero-g", "image_url": "https://images.unsplash.com/photo-1579952363873-27f3bade8f55?w=800", "action_url": "https://www.youtube.com/embed/Im_uKjC_eF8?autoplay=1"},
        {"title": "Neo-Tokyo United vs Mars Rovers", "category": "Soccer", "content_type": "live", "tags": "live,match,neo-tokyo", "image_url": "https://images.unsplash.com/photo-1517466787929-bc90951d6dbd?w=800", "action_url": "https://www.twitch.tv/mls"},
        {"title": "TICKET: Inter-Planetary Cup Semi", "category": "Soccer", "content_type": "ticket", "tags": "ticket,event,cup", "image_url": "https://images.unsplash.com/photo-1522778119026-d647f0565c6a?w=800", "action_url": "https://www.fifa.com/tickets"},
        {"title": "Boots: Anti-Gravity Cleats V5", "category": "Soccer", "content_type": "merchandise", "tags": "gear,shop,boots,tech", "image_url": "https://images.unsplash.com/photo-1511886929837-354d827aae26?w=800", "action_url": "https://www.adidas.com/us/soccer-shoes"},
        
        # --- ESPORTS ---
        {"title": "Drone Racing: Tokyo Drift 2077", "category": "eSports", "content_type": "video", "tags": "drone,racing,tokyo,speed", "image_url": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800", "action_url": "https://www.youtube.com/embed/WJ_p8k5zG5s?autoplay=1"},
        {"title": "VR Combat League: Global Final", "category": "eSports", "content_type": "live", "tags": "live,vr,combat,final", "image_url": "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=800", "action_url": "https://www.twitch.tv/riotgames"},
        {"title": "Headset: Neural Link Pro X", "category": "eSports", "content_type": "merchandise", "tags": "gear,shop,vr,tech", "image_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800", "action_url": "https://www.oculus.com/quest-2/"},
        {"title": "TICKET: LAN Party on The Moon", "category": "eSports", "content_type": "ticket", "tags": "ticket,event,vip", "image_url": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800", "action_url": "https://dreamhack.com/"},
        
        # --- RACING ---
        {"title": "Crash Compilation: 300MPH", "category": "Racing", "content_type": "video", "tags": "crash,highlights,racing", "image_url": "https://images.unsplash.com/photo-1532906619279-a764dccc8912?w=800", "action_url": "https://www.youtube.com/embed/fW4o8U8I89w?autoplay=1"},
        {"title": "Formula E: Electric Shock", "category": "Racing", "content_type": "video", "tags": "electric,racing,formula-e", "image_url": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800", "action_url": "https://www.youtube.com/embed/9g643v5w5_M?autoplay=1"},
        {"title": "TICKET: Neo-Monaco Grand Prix", "category": "Racing", "content_type": "ticket", "tags": "ticket,event,f1", "image_url": "https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?w=800", "action_url": "https://tickets.formula1.com/"},
        
        # --- NEW EXTENDED CONTENT (For Variety) ---
        {"title": "Sky-Boarding Championship 2077", "category": "Extreme", "content_type": "video", "tags": "extreme,sky,future", "image_url": "https://images.unsplash.com/photo-1522069213421-6925d8a284e3?w=800", "action_url": "https://www.youtube.com/embed/2GeF7A05zQ8?autoplay=1"},
        {"title": "Cyber-Yoga: Mind Upload", "category": "Fitness", "content_type": "article", "tags": "health,yoga,mind", "image_url": "https://images.unsplash.com/photo-1544367563-12123d8965cd?w=800", "action_url": "https://www.yogajournal.com/"},
        {"title": "Protein Synth: Lab Grown Gains", "category": "Fitness", "content_type": "merchandise", "tags": "shop,supplement,health", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800", "action_url": "https://www.gnc.com/"},
        {"title": "Robot Boxing: Steel Real", "category": "Combat", "content_type": "video", "tags": "boxing,robot,fight", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800", "action_url": "https://www.youtube.com/embed/Z1BCF89_wX0?autoplay=1"},
        {"title": "TICKET: Robot Wars Arena", "category": "Combat", "content_type": "ticket", "tags": "ticket,event,fight", "image_url": "https://images.unsplash.com/photo-1555597673-b21d5c935865?w=800", "action_url": "https://www.ticketmaster.com/"},
        {"title": "Hover-Bike Racing: League 1", "category": "Racing", "content_type": "live", "tags": "live,racing,hover", "image_url": "https://images.unsplash.com/photo-1558507652-2d9626c4e67a?w=800", "action_url": "https://www.twitch.tv/motorsport"},
        {"title": "AI Referee: The Controversy", "category": "Soccer", "content_type": "article", "tags": "ai,referee,news", "image_url": "https://images.unsplash.com/photo-1624880357913-a8539238245b?w=800", "action_url": "https://www.espn.com/"}
    ]

    for item in initial_content:
        db_item = ContentDB(**item)
        db.add(db_item)
    db.commit()
