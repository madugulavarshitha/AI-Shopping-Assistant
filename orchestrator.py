from typing import TypedDict, Annotated, Sequence, List, Dict, Any
import operator
import json
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from database.connection import SessionLocal
from models.product import Product
from models.category import Category
from models.review import Review
from models.price_history import PriceHistory

# Define the state of our Graph
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

import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini Model (Picks up GEMINI_API_KEY from environment variables)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY"),
    temperature=0.2
)

def extract_text(response) -> str:
    """Helper to safely extract string text from various LangChain message response formats."""
    if hasattr(response, "content"):
        content = response.content
    else:
        content = response
        
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                texts.append(block["text"])
            elif isinstance(block, str):
                texts.append(block)
        return "".join(texts)
    return str(content)

# --- Agents ---

def requirement_agent(state: AgentState):
    """Requirement Understanding Agent: Extracts shopping parameters, must-haves, nice-to-haves, etc."""
    query = state["user_query"]
    
    prompt = f"""
    You are the Requirement Understanding Agent of a coordinated multi-agent shopping intelligence system.
    Analyze the user's query: "{query}"
    
    Convert the natural-language query into structured shopping requirements and classify user intent.
    Intents:
    - "recommend": user is searching for products, looking for recommendations, or browsing.
    - "compare": user is asking to compare two or more products (e.g. "compare A and B").
    - "reviews": user wants customer reviews, ratings, pros and cons of a specific product.
    - "price": user wants price trends, price history, or buy/hold recommendation.
    - "general": greetings, chit-chat, or queries about assistant capabilities.
    
    Extract specifications and classify them into:
    1. MUST HAVE (mandatory features or budget limits)
    2. PREFERRED (preferred brands, colors, specs)
    3. NICE TO HAVE (secondary considerations)
    4. DEAL BREAKERS (conditions making products unsuitable)
    
    Return ONLY a valid JSON object matching this structure. Do not output anything else. If a field is not found, set it to null or an empty list.
    
    {{
        "intent": "recommend | compare | reviews | price | general",
        "category": "Exact match if applicable: Women's Fashion | Men's Fashion | Kids & Toys | Footwear | Electronics | Beauty & Grooming | Watches & Accessories | Home & Kitchen | Sports & Fitness | Books | null",
        "budget_max": maximum price limit (number or null),
        "budget_min": minimum price limit (number or null),
        "brand": "brand name if found, e.g. Apple, Zara, Levi's, Nike",
        "search_query": "general search terms for products",
        "products_to_compare": ["product name 1", "product name 2"],
        "target_product": "product name for reviews or price checking",
        "must_have": ["mandatory requirement 1", "mandatory requirement 2"],
        "preferred": ["preferred requirement 1", "preferred requirement 2"],
        "nice_to_have": ["nice to have 1"],
        "deal_breakers": ["deal breaker condition 1"]
    }}
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content_str = extract_text(response)
        clean_json = content_str.strip().replace("```json", "").replace("```", "")
        requirements = json.loads(clean_json)
    except Exception as e:
        print(f"Failed to extract requirements via LLM: {e}")
        lower_q = query.lower()
        intent = "recommend"
        if "compare" in lower_q or " vs " in lower_q or "versus" in lower_q:
            intent = "compare"
        elif "review" in lower_q or "rating" in lower_q or "feedback" in lower_q:
            intent = "reviews"
        elif "price" in lower_q or "deal" in lower_q or "discount" in lower_q or "trend" in lower_q:
            intent = "price"
        elif any(g in lower_q for g in ["hi", "hello", "hey", "help", "who are you"]):
            intent = "general"
            
        category = None
        if any(w in lower_q for w in ["women", "dress", "saree", "kurti", "skirt", "blouse", "female", "girl"]):
            category = "Women's Fashion"
        elif any(w in lower_q for w in ["men", "suit", "shirt", "blazer", "chino", "male", "boy"]):
            category = "Men's Fashion"
        elif any(w in lower_q for w in ["kid", "child", "toy", "lego", "frock", "dungaree"]):
            category = "Kids & Toys"
        elif any(w in lower_q for w in ["shoe", "sneaker", "running", "heel", "sandal", "footwear"]):
            category = "Footwear"
        elif any(w in lower_q for w in ["perfume", "serum", "dior", "dryer", "skincare", "beauty"]):
            category = "Beauty & Grooming"
        elif any(w in lower_q for w in ["kitchen", "home", "cookware", "air fryer", "blender", "coffee", "cooker", "kettle", "tawa", "purifier", "pillow", "bedsheet", "flask", "vacuum", "microwave", "appliance"]):
            category = "Home & Kitchen"
        elif any(w in lower_q for w in ["phone", "laptop", "headphone", "earphone", "macbook", "iphone", "electronics"]):
            category = "Electronics"

        requirements = {
            "intent": intent, 
            "category": category, 
            "budget_max": None, 
            "budget_min": None, 
            "brand": None,
            "search_query": query,
            "products_to_compare": [],
            "target_product": None,
            "must_have": [],
            "preferred": [],
            "nice_to_have": [],
            "deal_breakers": []
        }
    
    # Route based on intent
    intent = requirements.get("intent", "general")
    next_step = intent
    if intent not in ["recommend", "compare", "reviews", "price"]:
        next_step = "general"
        
    return {"extracted_requirements": requirements, "next_step": next_step}


def recommendation_agent(state: AgentState):
    """Recommendation Agent: Search catalog, score products using strict prompt formula, and rank."""
    reqs = state.get("extracted_requirements", {})
    query_text = state.get("user_query", "").lower()
    db = SessionLocal()
    recommended = []
    
    try:
        query = db.query(Product)
        
        # 1. Category Matching
        if reqs.get("category"):
            cat_name = reqs["category"].strip()
            cat = db.query(Category).filter(Category.name.ilike(f"{cat_name}%")).first()
            if not cat:
                cat = db.query(Category).filter(Category.name.ilike(f"%{cat_name}%")).first()
            if cat:
                query = query.filter(Product.category_id == cat.id)
                
        if reqs.get("brand"):
            query = query.filter(Product.brand.ilike(f"%{reqs['brand']}%"))
            
        # Deal breakers and budget must-haves
        if reqs.get("budget_max") is not None:
            query = query.filter(Product.price <= float(reqs["budget_max"]))
        if reqs.get("budget_min") is not None:
            query = query.filter(Product.price >= float(reqs["budget_min"]))
            
        products = query.all()
        
        # If strict filtering yields empty list, relax filters to return closest alternatives
        if not products:
            relaxed_query = db.query(Product)
            if reqs.get("category"):
                cat_name = reqs["category"].strip()
                cat = db.query(Category).filter(Category.name.ilike(f"{cat_name}%")).first()
                if not cat:
                    cat = db.query(Category).filter(Category.name.ilike(f"%{cat_name}%")).first()
                if cat:
                    relaxed_query = relaxed_query.filter(Product.category_id == cat.id)
            products = relaxed_query.all()
            if not products:
                products = db.query(Product).all()
                
        scored_products = []
        
        # Calculate score for each product based on requirements:
        for p in products:
            # 1. Requirement & Keyword Match (0.0 to 1.0)
            req_match = 0.5
            p_text = f"{p.name} {p.brand} {p.description} {p.category.name if p.category else ''}".lower()
            
            # Check if query keywords hit product name or description
            query_words = [w for w in query_text.replace(",", " ").replace(".", " ").split() if len(w) > 2]
            hit_count = sum(1 for w in query_words if w in p_text)
            if query_words:
                req_match = min(1.0, 0.4 + (hit_count / len(query_words)) * 0.6)
            else:
                req_match = 0.8
                
            if reqs.get("category") and p.category and reqs["category"].lower() in p.category.name.lower():
                req_match = min(1.0, req_match + 0.3)
                
            if reqs.get("brand") and reqs["brand"].lower() in p.brand.lower():
                req_match = min(1.0, req_match + 0.2)
                
            # 2. Feature Match (0.0 to 1.0)
            pref_matched = 0
            prefs = reqs.get("preferred", []) + reqs.get("must_have", [])
            if prefs:
                desc_lower = p.description.lower() if p.description else ""
                name_lower = p.name.lower()
                for pref in prefs:
                    if pref.lower() in desc_lower or pref.lower() in name_lower:
                        pref_matched += 1
                feature_match = pref_matched / len(prefs)
            else:
                feature_match = 0.9
                
            # 3. Value for Money (based on rating / price)
            val_for_money = (p.rating / 5.0) * (1.0 + p.discount / 100.0)
            val_for_money = min(val_for_money, 1.0)
            
            # 4. Review Sentiment (average rating ratio)
            rev_sentiment = p.rating / 5.0
            
            # 5. Performance / Brand Reputation
            perf = 0.8
            if p.brand.lower() in ["apple", "sony", "nike", "dior", "zara", "levi's", "raymond", "fabindia", "lego", "dyson"]:
                perf = 1.0
                
            # 6. Price Advantage
            price_advantage = 0.8
            if reqs.get("budget_max") is not None:
                budget = float(reqs["budget_max"])
                if budget > 0:
                    price_advantage = 1.0 - (p.price / budget)
                    price_advantage = max(0.1, min(price_advantage, 1.0))
            
            # Master Score Formula
            score = (
                req_match * 0.40 +
                feature_match * 0.20 +
                val_for_money * 0.10 +
                rev_sentiment * 0.10 +
                perf * 0.10 +
                price_advantage * 0.10
            )
            
            scored_products.append((p, score))
            
        # Rank by score descending
        scored_products.sort(key=lambda x: x[1], reverse=True)
        
        for p, score in scored_products[:4]:
            recommended.append({
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "original_price": p.original_price,
                "discount": p.discount,
                "rating": p.rating,
                "review_count": p.review_count,
                "image": p.image,
                "category": p.category.name if p.category else "Fashion",
                "recommendation_score": round(score * 100, 1)
            })
            
    except Exception as e:
        print(f"Recommendation Agent Error: {e}")
    finally:
        db.close()
        
    return {"recommended_products": recommended, "next_step": "buy_guide"}


def compare_agent(state: AgentState):
    """Comparison Agent: Normalizes specs and compiles side-by-side properties."""
    reqs = state.get("extracted_requirements", {})
    to_compare = reqs.get("products_to_compare", [])
    db = SessionLocal()
    compare_results = []
    
    try:
        products = []
        if to_compare:
            for name in to_compare:
                p = db.query(Product).filter(Product.name.ilike(f"%{name}%")).first()
                if p:
                    products.append(p)
                    
        # Fallback if names didn't match or were empty
        if not products:
            category_name = reqs.get("category")
            if category_name:
                cat = db.query(Category).filter(Category.name.ilike(f"%{category_name}%")).first()
                if cat:
                    products = db.query(Product).filter(Product.category_id == cat.id).limit(2).all()
            if not products:
                products = db.query(Product).limit(2).all()
                
        for p in products:
            specs = json.loads(p.specifications) if p.specifications else {}
            compare_results.append({
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "original_price": p.original_price,
                "discount": p.discount,
                "rating": p.rating,
                "review_count": p.review_count,
                "image": p.image,
                "category": p.category.name if p.category else "Electronics",
                "specifications": specs,
                "warranty": specs.get("Warranty", "1 Year"),
                "color": specs.get("Color", "Standard"),
                "weight": specs.get("Weight", "Standard")
            })
            
    except Exception as e:
        print(f"Compare Agent Error: {e}")
    finally:
        db.close()
        
    return {"comparison_results": compare_results, "next_step": "buy_guide"}


def reviews_agent(state: AgentState):
    """Review Summarization Agent: Identifies positive/negative themes and customer consensus."""
    reqs = state.get("extracted_requirements", {})
    target = reqs.get("target_product") or reqs.get("search_query")
    db = SessionLocal()
    review_summary = {}
    
    try:
        product = None
        if target:
            product = db.query(Product).filter(Product.name.ilike(f"%{target}%")).first()
            if not product:
                product = db.query(Product).filter(Product.name.ilike(f"%{target.split()[0]}%")).first()
                
        if not product:
            # Fallback to first available product
            product = db.query(Product).first()
            
        if product:
            reviews = db.query(Review).filter(Review.product_id == product.id).all()
            review_list = []
            positive_themes = []
            negative_themes = []
            
            for r in reviews:
                review_list.append({
                    "rating": r.rating,
                    "text": r.review_text,
                    "sentiment": r.sentiment,
                    "user": r.user.name if r.user else "Anonymous"
                })
                if r.sentiment == "Positive" and len(positive_themes) < 3:
                    positive_themes.append(r.review_text)
                elif r.sentiment == "Negative" and len(negative_themes) < 3:
                    negative_themes.append(r.review_text)
                    
            review_summary = {
                "product_name": product.name,
                "product_id": product.id,
                "average_rating": product.rating,
                "review_count": product.review_count,
                "positive_themes": positive_themes if positive_themes else ["Great build quality", "Very satisfied"],
                "negative_themes": negative_themes if negative_themes else ["Slightly expensive", "Delivery took time"],
                "overall_sentiment": "Positive" if product.rating >= 4.5 else ("Mixed" if product.rating >= 3.5 else "Negative"),
                "reviews": review_list
            }
        else:
            review_summary = {"error": "Customer review analysis is unavailable for this product."}
            
    except Exception as e:
        print(f"Reviews Agent Error: {e}")
        review_summary = {"error": "Customer review analysis is unavailable for this product."}
    finally:
        db.close()
        
    return {"review_summary": review_summary, "next_step": "buy_guide"}


def price_agent(state: AgentState):
    """Price Intelligence Agent: Classifies price attractiveness and timing signals."""
    reqs = state.get("extracted_requirements", {})
    target = reqs.get("target_product") or reqs.get("search_query")
    db = SessionLocal()
    price_analysis = {}
    
    try:
        product = None
        if target:
            product = db.query(Product).filter(Product.name.ilike(f"%{target}%")).first()
            if not product:
                product = db.query(Product).filter(Product.name.ilike(f"%{target.split()[0]}%")).first()
                
        if not product:
            product = db.query(Product).first()
            
        if product:
            history_records = db.query(PriceHistory).filter(PriceHistory.product_id == product.id).order_by(PriceHistory.recorded_at.asc()).all()
            prices = [ph.price for ph in history_records]
            
            if prices:
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                current_price = product.price
                
                # Attractiveness classification
                if current_price <= min_price * 1.02:
                    price_deal_class = "VERY GOOD DEAL"
                    buy_signal = "BUY NOW"
                    reason = "This price is at its historic lowest value. Waiting is not recommended."
                elif current_price < avg_price:
                    price_deal_class = "GOOD DEAL"
                    buy_signal = "BUY"
                    reason = "Price is currently below the historical average."
                elif abs(current_price - avg_price) / avg_price <= 0.05:
                    price_deal_class = "FAIR PRICE"
                    buy_signal = "HOLD"
                    reason = "Price is fair and close to the historical average."
                else:
                    price_deal_class = "EXPENSIVE"
                    buy_signal = "WAIT"
                    reason = "Price is currently high. Based on historical data, waiting for a drop is reasonable."
                
                price_analysis = {
                    "product_name": product.name,
                    "product_id": product.id,
                    "current_price": current_price,
                    "original_price": product.original_price or current_price,
                    "discount": product.discount,
                    "average_price": round(avg_price, 2),
                    "min_price": min_price,
                    "max_price": max(prices),
                    "price_deal_class": price_deal_class,
                    "buy_signal": buy_signal,
                    "reason": reason,
                    "history": [{"price": ph.price, "date": ph.recorded_at.strftime("%Y-%m-%d")} for ph in history_records]
                }
            else:
                price_analysis = {
                    "product_name": product.name,
                    "product_id": product.id,
                    "current_price": product.price,
                    "original_price": product.original_price or product.price,
                    "discount": product.discount,
                    "price_deal_class": "INSUFFICIENT PRICE DATA",
                    "buy_signal": "HOLD",
                    "reason": "Insufficient historical data to determine whether this is the best time to buy."
                }
        else:
            price_analysis = {"error": "Pricing details are currently unavailable."}
            
    except Exception as e:
        print(f"Price Agent Error: {e}")
        price_analysis = {"error": "Pricing details are currently unavailable."}
    finally:
        db.close()
        
    return {"price_analysis": price_analysis, "next_step": "buy_guide"}


def buying_guidance_agent(state: AgentState):
    """Buying Guidance Agent: Generates final response using a clean JSON format."""
    reqs = state.get("extracted_requirements", {})
    intent = reqs.get("intent", "general")
    query = state["user_query"]
    
    # Compile DB results to pass to Gemini
    context_data = {
        "user_query": query,
        "extracted_requirements": reqs,
        "recommended_products": state.get("recommended_products", []),
        "comparison_results": state.get("comparison_results", []),
        "review_summary": state.get("review_summary", {}),
        "price_analysis": state.get("price_analysis", {})
    }
    
    prompt = f"""
    You are the final Buying Guidance Agent of a coordinated multi-agent e-commerce shopping system.
    Generate the shopping response to the query: "{query}"
    
    Database details:
    {json.dumps(context_data, indent=2)}
    
    You MUST output ONLY a valid JSON object matching this structure. Do not output anything else. No backticks, no markdown.
    If a field is not found or not applicable, set it to null or an empty list.
    
    {{
        "message": "A friendly, professional conversational greeting/intro summarizing the search and results, e.g. 'I found some great options for you! ✨' or 'Here is a comparison of those products for you.'",
        "recommended_product_id": integer ID of the best recommended product (number or null),
        "pros": ["pro of recommended product 1", "pro of recommended product 2"],
        "cons": ["con of recommended product 1", "con of recommended product 2"],
        "comparison_verdict": "comparison summary sentence if applicable, else null",
        "verdict": "A brief conclusion explaining why the recommended product is the best choice and outlining key trade-offs."
    }}
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        response_text = extract_text(response)
    except Exception as e:
        print(f"LLM compilation error: {e}")
        fallback_data = {
            "message": "I processed your request, but hit a temporary issue compiling detailed AI insights. However, you can check the catalog or search query directly!",
            "recommended_product_id": None,
            "pros": [],
            "cons": [],
            "comparison_verdict": None,
            "verdict": "Explore the catalog categories and compare items directly on the dashboard."
        }
        response_text = json.dumps(fallback_data)
        
    return {"final_response": response_text, "next_step": "end"}

# --- Orchestrator Setup ---

def route_next(state: AgentState):
    ns = state.get("next_step")
    if ns == "recommend":
        return "recommendation_agent"
    elif ns == "compare":
        return "compare_agent"
    elif ns == "reviews":
        return "reviews_agent"
    elif ns == "price":
        return "price_agent"
    elif ns == "general":
        return "buying_guidance_agent"
    elif ns == "buy_guide":
        return "buying_guidance_agent"
    return END

workflow = StateGraph(AgentState)

workflow.add_node("requirement_agent", requirement_agent)
workflow.add_node("recommendation_agent", recommendation_agent)
workflow.add_node("compare_agent", compare_agent)
workflow.add_node("reviews_agent", reviews_agent)
workflow.add_node("price_agent", price_agent)
workflow.add_node("buying_guidance_agent", buying_guidance_agent)

workflow.set_entry_point("requirement_agent")
workflow.add_conditional_edges("requirement_agent", route_next)
workflow.add_edge("recommendation_agent", "buying_guidance_agent")
workflow.add_edge("compare_agent", "buying_guidance_agent")
workflow.add_edge("reviews_agent", "buying_guidance_agent")
workflow.add_edge("price_agent", "buying_guidance_agent")
workflow.add_edge("buying_guidance_agent", END)

app = workflow.compile()

def run_orchestrator(query: str):
    initial_state = {
        "user_query": query,
        "messages": [HumanMessage(content=query)],
        "extracted_requirements": {},
        "recommended_products": [],
        "comparison_results": [],
        "review_summary": {},
        "price_analysis": {},
        "final_response": "",
        "next_step": ""
    }
    
    result = app.invoke(initial_state)
    
    # Parse guidance JSON
    raw_response = result.get("final_response", "")
    try:
        clean_json = raw_response.strip().replace("```json", "").replace("```", "").strip()
        guidance = json.loads(clean_json)
    except Exception as e:
        print(f"Failed to parse guidance JSON: {e}. Raw response was: {raw_response}")
        guidance = {
            "message": raw_response if raw_response else "I analyzed the catalog for your request.",
            "recommended_product_id": None,
            "pros": [],
            "cons": [],
            "comparison_verdict": None,
            "verdict": "Explore the catalog categories and compare items directly on the dashboard."
        }
        
    # Map recommendations/comparisons to display inside UI chat cards
    products_to_return = []
    if result.get("recommended_products"):
        products_to_return = result["recommended_products"]
    elif result.get("comparison_results"):
        products_to_return = result["comparison_results"]
    elif result.get("review_summary") and result["review_summary"].get("product_id"):
        db = SessionLocal()
        try:
            p = db.query(Product).filter(Product.id == result["review_summary"]["product_id"]).first()
            if p:
                products_to_return = [{
                    "id": p.id,
                    "name": p.name,
                    "brand": p.brand,
                    "price": p.price,
                    "original_price": p.original_price,
                    "discount": p.discount,
                    "rating": p.rating,
                    "review_count": p.review_count,
                    "image": p.image
                }]
        finally:
            db.close()
    elif result.get("price_analysis") and result["price_analysis"].get("product_id"):
        db = SessionLocal()
        try:
            p = db.query(Product).filter(Product.id == result["price_analysis"]["product_id"]).first()
            if p:
                products_to_return = [{
                    "id": p.id,
                    "name": p.name,
                    "brand": p.brand,
                    "price": p.price,
                    "original_price": p.original_price,
                    "discount": p.discount,
                    "rating": p.rating,
                    "review_count": p.review_count,
                    "image": p.image
                }]
        finally:
            db.close()
            
    # Build structured response structure
    structured_data = {
        "type": result["extracted_requirements"].get("intent", "general"),
        "message": guidance.get("message", ""),
        "verdict": guidance.get("verdict", ""),
        "recommended_product_id": guidance.get("recommended_product_id"),
        "pros": guidance.get("pros", []),
        "cons": guidance.get("cons", []),
        "products": products_to_return,
        "comparison": None,
        "price_analysis": None,
        "review_summary": None
    }
    
    # 1. Comparison mapping
    comp_results = result.get("comparison_results", [])
    if comp_results:
        headers = ["Feature"] + [p["name"] for p in comp_results]
        features = ["Price", "Rating", "Brand", "Warranty", "Color", "Weight"]
        rows = []
        for f in features:
            row = [f]
            for p in comp_results:
                specs = p.get("specifications") or {}
                val = ""
                if f == "Price":
                    val = f"₹{int(p['price']):,}" if p.get('price') else "N/A"
                elif f == "Rating":
                    val = f"★ {p['rating']}" if p.get('rating') else "N/A"
                elif f == "Brand":
                    val = p.get("brand") or "N/A"
                elif f == "Warranty":
                    val = p.get("warranty") or specs.get("Warranty") or "1 Year"
                elif f == "Color":
                    val = p.get("color") or specs.get("Color") or "Standard"
                elif f == "Weight":
                    val = p.get("weight") or specs.get("Weight") or "Standard"
                row.append(val)
            rows.append(row)
            
        # Add AI Verdict row
        best_id = guidance.get("recommended_product_id")
        verdict_row = ["AI Verdict"]
        for p in comp_results:
            if best_id and p["id"] == best_id:
                verdict_row.append("🏆 Recommended")
            else:
                verdict_row.append("Alternative")
        rows.append(verdict_row)
        
        structured_data["comparison"] = {
            "headers": headers,
            "rows": rows,
            "verdict": guidance.get("comparison_verdict", "")
        }
        
    # 2. Price analysis mapping
    pa = result.get("price_analysis", {})
    if pa and "error" not in pa and pa.get("product_id") is not None:
        prob_map = {"VERY GOOD DEAL": 95, "GOOD DEAL": 80, "FAIR PRICE": 50, "EXPENSIVE": 20, "INSUFFICIENT PRICE DATA": 50}
        buy_sig = pa.get("buy_signal", "HOLD")
        price_deal_class = pa.get("price_deal_class", "FAIR PRICE")
        structured_data["price_analysis"] = {
            "product_id": pa.get("product_id"),
            "product_name": pa.get("product_name"),
            "current_price": pa.get("current_price"),
            "lowest_price": pa.get("min_price"),
            "average_price": pa.get("average_price"),
            "highest_price": pa.get("max_price"),
            "buy_signal": buy_sig,
            "buy_probability": prob_map.get(price_deal_class, 50),
            "reason": pa.get("reason"),
            "history": pa.get("history", [])
        }
        
    # 3. Review summary mapping
    rs = result.get("review_summary", {})
    if rs and "error" not in rs and rs.get("product_id") is not None:
        structured_data["review_summary"] = {
            "product_id": rs.get("product_id"),
            "product_name": rs.get("product_name"),
            "average_rating": rs.get("average_rating"),
            "review_count": rs.get("review_count"),
            "pros": rs.get("positive_themes", []),
            "cons": rs.get("negative_themes", []),
            "overall_sentiment": rs.get("overall_sentiment", "Neutral")
        }
        
    # Backward compatible plain-text response (for standard chat bubbles fallback)
    fallback_text = guidance.get("message", "")
    if guidance.get("verdict"):
        fallback_text += f"\n\n**Verdict:** {guidance.get('verdict')}"
        
    return {
        "text": fallback_text,
        "products": products_to_return,
        "structured_data": structured_data
    }
