# Model/API Keys (required for ADK/Gemini)
GOOGLE_API_KEY="your_google_api_key_here"  # For Gemini models via google-generativeai
GEMINI_MODEL_ENDPOINT=https://generativelanguage.googleapis.com/  # Optional override

# Tool Keys (for researcher, recommendation agents)
PUBMED_API_KEY="your_pubmed_key"  # If using NCBI E-utilities for medical research
TAVILY_API_KEY="your_tavily_key"  # For hybrid search in researcher (if integrated)
GOOGLE_MAPS_API_KEY="your_maps_key"  # For hospital recommendations in geo_tools.py

# Database/Memory (for session state, reflection agent)
QDRANT_URL=http://localhost:6333  # Or cloud URL
QDRANT_API_KEY="your_qdrant_key"
REDIS_URL="redis://localhost:6379/0"  # If using Redis for caching

# App Configs
LOG_LEVEL="DEBUG"  # Or INFO, ERROR for logging.py
APP_PORT=8000  # For api.py if using FastAPI
ENVIRONMENT="development"  # Or production to toggle behaviors