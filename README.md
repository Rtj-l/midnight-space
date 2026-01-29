# Midnight Space - Intelligent Content Recommendation Engine 🌌

A next-generation content platform featuring real-time biometric simulation, dynamic content injection, and a visually immersive "Cyber-Nebula" interface.

## 🚀 Quick Start (Windows)

1.  **Double-click `run_demo.bat`**
    *   This will automatically install dependencies, reset the database, and launch the server.
2.  Open your browser to: `http://localhost:8000`

## 🐳 Docker Deployment

To run in a containerized environment (e.g., Google Cloud Run):

```bash
cd backend
docker build -t midnight-space .
docker run -p 8080:8080 midnight-space
```

## ✨ Key Features

1.  **Hybrid Recommendation Engine**: Combines content-based filtering (TF-IDF) with simulated collaborative signals.
2.  **Dynamic "Rule 16" Injection**: The feed reacts instantly to your interactions. "Like" a video, and see related content appear immediately with a "BECAUSE YOU LIKED THIS" separator.
3.  **Immersive UI**:
    *   **Hyper-Dynamic Background**: A nebula that shifts colors every 10 seconds.
    *   **Retro-Futuristic Grid**: A scanning grid overlay for depth.
    *   **Glitch Typography**: Custom fonts and animations.
4.  **Robust Playback**: Automatically converts YouTube URLs to embed-safe formats for seamless viewing.

## 🛠️ Tech Stack

*   **Backend**: FastAPI (Python), SQLite, Scikit-Learn
*   **Frontend**: Vanilla JS, CSS3 (No heavy frameworks), HTML5
*   **Deployment**: Docker-ready
