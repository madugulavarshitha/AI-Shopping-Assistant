AI Shopping Assistant

Generative AI-Powered Product Discovery & Buying Guidance System
A full-stack, multi-agent shopping platform that helps users discover
products, compare options, understand reviews, and make price-aware
buying decisions.

📌 Overview

Online shopping platforms contain thousands of products with different
specifications, prices, ratings, and customer reviews. Comparing
products across multiple pages can be time-consuming and can still
result in uncertain purchasing decisions.

The AI Shopping Assistant solves this problem through a coordinated
team of specialized AI agents. A LangGraph-based Orchestrator Agent
interprets each user query and routes it to the appropriate specialized
agent.

The system combines:

Google Gemini for generative AI reasoning
LangGraph / LangChain for multi-agent orchestration
FastAPI for backend APIs
React + TypeScript + Vite for the frontend
Tailwind CSS for UI styling
SQLAlchemy for database access
SQLite / PostgreSQL for product and transaction data
Qdrant for potential vector-based semantic search

The platform provides personalized recommendations, side-by-side
comparisons, review summaries, price intelligence, and buying guidance
through a persistent AI Assistant chat panel.

✨ Key Features
🤖 Multi-agent AI shopping assistant
🎯 Personalized product recommendations
⚖️ Side-by-side product comparison
⭐ Customer review summarization and sentiment analysis
💰 Historical price intelligence
🛒 Cart and checkout management
❤️ Wishlist management
📦 Order history
🔎 Product and catalog search
💬 Persistent AI Assistant chat panel
📊 AI Match percentage for recommendations
📈 Historical price trend visualization
🧠 AI-powered BUY / HOLD / WAIT guidance
🔐 JWT-based authentication
🏗️ System Architecture
┌──────────────────────────────┐
│ React + TypeScript Frontend  │
│ Vite + Tailwind CSS          │
└──────────────┬───────────────┘
               │ REST / JSON
               ▼
┌──────────────────────────────┐
│ FastAPI Backend              │
│ Authentication / Products    │
│ Categories / Cart / Orders   │
│ Reviews / Chat               │
└──────────────┬───────────────┘
               │ Request
               ▼
┌──────────────────────────────┐
│ LangGraph Orchestrator       │
│ StateGraph + Intent Routing  │
└──────────────┬───────────────┘
               │
       ┌───────┴────────────────────────────────────┐
       ▼       ▼        ▼        ▼        ▼         ▼
   Requirement Recommendation Comparison Reviews  Price  Buying
   Agent      Agent        Agent      Agent   Agent  Guidance
       │       │        │        │        │         │
       └───────┴────────┴────────┴────────┴─────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Google Gemini          Product Database
                              SQLite/PostgreSQL

The architecture follows the project documentation's flow:

React + TypeScript → FastAPI → LangGraph → Specialized Agents → Gemini
/ Database → Response to Frontend.

🤖 Specialized AI Agents

The system contains six specialized agents.

1. Requirement Understanding Agent

Converts natural-language shopping queries into structured requirements.

It identifies:

Intent
Category
Budget range
Brand
Must-have features
Preferred features
Nice-to-have features
Deal breakers

It uses a JSON-oriented response contract and includes keyword-based
intent detection as a fallback when the LLM call fails.

2. Recommendation Agent

Filters and ranks products according to the user's requirements.

The scoring formula is:

Factor Weight

Requirement match 40%
Feature match 20%
Value for money 10%
Review sentiment 10%
Brand performance 10%
Price advantage 10%

The agent returns the top four ranked products.

3. Comparison Agent

Compares selected products and normalizes their information into a
side-by-side structure.

Comparison information includes:

Price
Rating
Warranty
Color
Weight
Product specifications

The UI also displays an AI Verdict identifying the recommended
option.

4. Review Summarization Agent

Analyzes customer reviews for a product and extracts:

Positive themes
Negative themes
Overall sentiment

Sentiment is classified as:

Positive
Mixed
Negative
5. Price Intelligence Agent

Analyzes historical product prices.

It calculates:

Average historical price
Minimum historical price
Current price position

The current price is classified as:

VERY GOOD DEAL
GOOD DEAL
FAIR PRICE
EXPENSIVE

The agent also provides a buying signal such as:

BUY NOW
BUY
HOLD
WAIT
6. Buying Guidance Agent

Combines the outputs of the other agents and generates the final
structured buying recommendation.

The final output can include:

Message
Recommended product ID
Pros
Cons
Comparison verdict
Final verdict
🔄 LangGraph Orchestration

The orchestrator uses a shared AgentState:

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_query: str
    extracted_requirements: Dict[str, Any]
    recommended_products: List[Dict[str, Any]]
    comparison_results: List[Dict[str, Any]]
    review_summary: Dict[str, Any]
    price_analysis: Dict[str, Any]
    final_response: str
    next_step: str

The graph contains nodes for:

Requirement Understanding
          │
          ▼
     Intent Router
     ┌────┼────┬────┐
     ▼    ▼    ▼    ▼
Recommend Compare Reviews Price
     │    │    │    │
     └────┴────┴────┘
          ▼
  Buying Guidance
          │
          ▼
       Response

The orchestrator routes requests based on detected intent:

recommend
compare
reviews
price
general
buy_guide
💡 Example Use Cases
Recommendation

User:

Suggest a laptop under ₹90,000 for college.

The Requirement Understanding Agent extracts the category and budget.
The Recommendation Agent ranks matching products, and the Buying
Guidance Agent provides the final recommendation.

Product Comparison

User:

Compare iPhone 15 Pro and Sony WH-1000XM5.

The Comparison Agent retrieves both products, normalizes their
specifications, and returns a side-by-side comparison with an AI
Verdict.

Price Intelligence

User:

Is this saree a good time to buy?

The Price Intelligence Agent analyzes historical prices and provides a
price classification and BUY / HOLD / WAIT signal.

Review Analysis

User:

What do customers think about this product?

The Review Summarization Agent analyzes product reviews and returns
positive themes, negative themes, and an overall sentiment
classification.

🖥️ Frontend

The frontend is built using:

React
TypeScript
Vite
Tailwind CSS
React Router
Axios
TanStack React Query
Recharts
Framer Motion
Lucide React
Main Pages
Landing
Sign Up
Sign In
Forgot Password
Reset Password
Home
Categories
Recommendations
Compare
Reviews
Price Intelligence
Deals & Offers
Orders
Wishlist
Cart
Profile
Product Details
Search Results

The authenticated dashboard uses a persistent sidebar and a persistent
AI Assistant panel.

🔌 Backend API

The FastAPI backend exposes routes for:

/api/auth
/api/products
/api/categories
/api/chat
/api/cart
/api/wishlist
/api/orders
/api/reviews
AI Chat Endpoint
POST /api/chat

Request:

{
  "message": "Suggest a laptop under 90000 for college",
  "history": []
}

Response structure:

{
  "response": "...",
  "recommended_products": [],
  "structured_data": {}
}
🔐 Authentication

The application uses JWT-based authentication.

Authentication functionality includes:

User signup
User login
Current-user retrieval
Password hashing
Protected user-specific resources

The authentication implementation uses python-jose and
bcrypt/passlib-based password hashing.

🗄️ Database

The application supports SQLite and PostgreSQL.

Example local configuration:

DATABASE_URL=sqlite:///./ai_shopping.db
JWT_SECRET=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=http://localhost:6333

The database contains data for:

Categories
Products
Reviews
Price history
Cart
Wishlist
Orders
Users
🧰 Prerequisites

Before running the project, familiarity with the following is useful:

Python
FastAPI
React
TypeScript
Node.js and npm
LangChain
LangGraph
Google Gemini API
SQLAlchemy
Relational databases
Tailwind CSS
Git
🚀 Installation
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
2. Backend Setup

Navigate to the backend:

cd backend

Create a virtual environment:

python -m venv venv
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
3. Configure Backend Environment

Create:

backend/.env

Add:

DATABASE_URL=sqlite:///./ai_shopping.db
JWT_SECRET=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=http://localhost:6333

Never commit your real API key or secrets to GitHub.

4. Seed the Database

From the backend directory:

python database/seed.py
5. Start the Backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000

Backend:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
6. Frontend Setup

Open another terminal and navigate to:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Frontend:

http://127.0.0.1:5173
📦 Important Dependencies
Backend
fastapi
uvicorn
sqlalchemy
python-dotenv
python-jose[cryptography]
bcrypt
google-genai
google-generativeai
langchain
langchain-core
langchain-google-genai
langgraph
qdrant-client
Frontend
react
react-router-dom
axios
@tanstack/react-query
recharts
framer-motion
lucide-react
tailwindcss
🔑 Gemini API Configuration

Create a Gemini API key and store it in the backend environment file:

GEMINI_API_KEY=your_gemini_api_key
LLM_API_KEY=your_gemini_api_key

The application loads environment variables using python-dotenv.

Example configuration:

from dotenv import load_dotenv
import os

load_dotenv()

Security: Never commit .env files, API keys, JWT secrets,
database credentials, or other secrets to GitHub.

Add the following to .gitignore:

.env
*.env
venv/
__pycache__/
node_modules/
frontend/dist/
*.db
🏭 Production Build

Build the frontend:

npm run build

The production assets are generated in:

frontend/dist

Preview the production build:

npm run preview
🧪 End-to-End Verification

After starting the application:

Create a user account.
Sign in.
Verify JWT session persistence.
Browse the Home page.
Browse Categories.
Open product details.
Test product recommendations.
Test product comparisons.
Test review analysis.
Test price intelligence.
Add products to Cart.
Add products to Wishlist.
Test checkout.
Verify Orders.
Test the persistent AI Assistant.

Example AI queries:

Suggest a laptop under 90000 for college.
Compare two products.
What do customers think about this product?
Is this product a good time to buy?
📊 AI Assistant Response

The AI Assistant can render structured results including:

AI-recommended product cards
AI Match percentage
Product price
Product rating
Comparison tables
Price trend summaries
BUY / HOLD / WAIT guidance
Review strengths
Review weaknesses
Sentiment
Final AI Verdict
🛒 E-Commerce Features
Cart

The Cart provides a checkout flow:

Cart List
    ↓
Address Details
    ↓
Mock Payment

The price summary includes:

Subtotal
Delivery charges
Estimated GST
Total amount
Wishlist

Users can save products using the wishlist feature and move back to
product browsing when needed.

Orders

The Orders page displays the user's purchase history.

📈 Future Enhancements

Potential extensions include:

Vector-based semantic search using Qdrant / FAISS
Richer personalization
More advanced recommendation strategies
Production-grade payment integration
Real-time product and price data
Additional AI shopping agents
Advanced user preference learning
📁 Suggested Project Structure
AI-Shopping-Assistant/
│
├── backend/
│   ├── agents/
│   ├── database/
│   ├── routers/
│   ├── orchestrator.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
🛠️ Development Workflow
Phase 1 --- Model Selection & Architecture
Configure Gemini API
Select the generative AI model
Design the multi-agent architecture
Set up backend and frontend dependencies
Phase 2 --- Core Agent Development
Develop six specialized agents
Implement FastAPI routers
Connect agents to product data
Phase 3 --- Orchestration
Build the LangGraph StateGraph
Add conditional routing
Connect agent outputs
Generate final buying guidance
Phase 4 --- Frontend
Build the dashboard
Add product pages
Add AI Assistant
Add comparison, reviews, and price intelligence views
Connect frontend to backend APIs
Phase 5 --- Deployment
Configure environment variables
Seed the database
Run and test the backend
Build and serve the frontend
Perform end-to-end verification
📚 Technologies Used

Technology Purpose

Python Backend and AI agent development
FastAPI REST API backend
LangGraph Agent orchestration
LangChain LLM and agent integration
Google Gemini Generative AI reasoning
React Frontend UI
TypeScript Frontend type safety
Vite Frontend build/development
Tailwind CSS UI styling
SQLAlchemy ORM
SQLite Local database
PostgreSQL Relational database option
Qdrant Vector search extension
React Query Data fetching and caching
Recharts Price history visualization
JWT Authentication

🎯 Project Objective

The goal of the AI Shopping Assistant is to reduce the complexity of
online shopping by combining product data, customer feedback, historical
pricing, and generative AI into a single conversational experience.

Instead of manually comparing products across multiple pages, users can
ask the AI Assistant natural-language questions and receive
personalized, structured, and actionable shopping guidance.


👨‍💻 Project

AI Shopping Assistant
Generative AI-Powered Product Discovery & Buying Guidance System

Built with FastAPI + LangGraph + Google Gemini + React + TypeScript.
