AI Shopping Assistant

AI-powered shopping assistant for smarter product decisions.

Features
Product recommendations
Product comparison
Review analysis
Price analysis
AI shopping chat
Cart and Wishlist
Orders
Tech Stack

Frontend: React, TypeScript, Tailwind CSS
Backend: FastAPI, Python
AI: Google Gemini, LangGraph
Database: SQLite / PostgreSQL

AI Agents
Requirement Agent
Recommendation Agent
Comparison Agent
Review Agent
Price Agent
Buying Guidance Agent
Run
Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Frontend
cd frontend
npm install
npm run dev
Environment

Create backend/.env:

GEMINI_API_KEY=your_api_key
DATABASE_URL=sqlite:///./ai_shopping.db
