import re
from typing import List, Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.product import Product
from models.category import Category

# Comprehensive synonym and stemming dictionary (strict semantic equivalents)
SYNONYMS_AND_STEMS: Dict[str, List[str]] = {
    # Tech & Laptops
    "laptops": ["laptop", "notebook", "macbook", "ultrabook", "chromebook"],
    "laptop": ["laptop", "notebook", "macbook", "ultrabook", "chromebook"],
    "macbooks": ["macbook", "apple", "laptop"],
    "macbook": ["macbook", "apple", "laptop"],
    "computers": ["computer", "pc", "desktop"],
    "computer": ["computer", "pc", "desktop"],
    "pc": ["pc", "computer", "desktop"],
    "ultrabooks": ["ultrabook", "laptop"],
    "ultrabook": ["ultrabook", "laptop"],
    
    # Phones & Mobile
    "phones": ["phone", "smartphone", "iphone", "mobile"],
    "phone": ["phone", "smartphone", "iphone", "mobile"],
    "mobiles": ["mobile", "phone", "smartphone"],
    "mobile": ["mobile", "phone", "smartphone"],
    "smartphones": ["smartphone", "phone", "mobile"],
    "smartphone": ["smartphone", "phone", "mobile"],
    "iphones": ["iphone", "apple", "phone"],
    "iphone": ["iphone", "apple", "phone"],
    
    # Audio & TV
    "headphones": ["headphone", "audio", "earphone", "earbuds", "headset"],
    "headphone": ["headphone", "audio", "earphone", "earbuds", "headset"],
    "earphones": ["earphone", "headphone", "earbuds", "headset"],
    "earphone": ["earphone", "headphone", "earbuds", "headset"],
    "earbuds": ["earbuds", "earphone", "headphone", "airpods"],
    "earbud": ["earbuds", "earphone", "headphone", "airpods"],
    "tvs": ["tv", "television", "smart tv"],
    "tv": ["tv", "television", "smart tv"],
    "televisions": ["television", "tv", "smart tv"],
    "television": ["television", "tv", "smart tv"],
    
    # Women's Fashion
    "sarees": ["saree", "sari"],
    "saree": ["saree", "sari"],
    "saris": ["saree", "sari"],
    "sari": ["saree", "sari"],
    "dresses": ["dress", "gown", "frock", "maxi"],
    "dress": ["dress", "gown", "frock", "maxi"],
    "gowns": ["gown", "dress"],
    "gown": ["gown", "dress"],
    "frocks": ["frock", "dress"],
    "frock": ["frock", "dress"],
    "chudidhars": ["chudidhar", "churidar", "salwar", "kurti"],
    "chudidhar": ["chudidhar", "churidar", "salwar", "kurti"],
    "churidars": ["chudidhar", "churidar", "salwar", "kurti"],
    "churidar": ["chudidhar", "churidar", "salwar", "kurti"],
    "salwar": ["salwar", "chudidhar", "churidar", "kurti"],
    "salwars": ["salwar", "chudidhar", "churidar", "kurti"],
    "suits": ["suit", "salwar", "chudidhar"],
    "suit": ["suit", "salwar", "chudidhar"],
    "kurtis": ["kurti", "kurta", "chudidhar"],
    "kurti": ["kurti", "kurta", "chudidhar"],
    "kurtas": ["kurta", "kurti"],
    "kurta": ["kurta", "kurti"],
    "bags": ["bag", "handbag", "purse", "tote"],
    "bag": ["bag", "handbag", "purse", "tote"],
    "handbags": ["handbag", "bag", "purse", "tote"],
    "handbag": ["handbag", "bag", "purse", "tote"],
    "jeans": ["jeans", "denim", "pants"],
    "denim": ["denim", "jeans"],
    
    # Footwear & Men's
    "shoes": ["shoe", "sneaker", "footwear"],
    "shoe": ["shoe", "sneaker", "footwear"],
    "sneakers": ["sneaker", "shoe", "footwear"],
    "sneaker": ["sneaker", "shoe", "footwear"],
    "footwear": ["footwear", "shoe", "sneaker"],
    "shirts": ["shirt", "polo"],
    "shirt": ["shirt", "polo"],
    "tshirts": ["t-shirt", "tshirt", "tee"],
    "tshirt": ["t-shirt", "tshirt", "tee"],
    "tees": ["t-shirt", "tshirt", "tee"],
    "tee": ["t-shirt", "tshirt", "tee"],
    
    # Home Appliances
    "fridges": ["refrigerator", "fridge"],
    "fridge": ["refrigerator", "fridge"],
    "refrigerators": ["refrigerator", "fridge"],
    "refrigerator": ["refrigerator", "fridge"],
    "washers": ["washing machine", "washer"],
    "washing": ["washing machine", "washer"],
    "acs": ["air conditioner", "ac"],
    "ac": ["air conditioner", "ac"],
    "vacuums": ["vacuum", "cleaner"],
    "vacuum": ["vacuum", "cleaner"],
    "fryers": ["air fryer", "fryer"],
    "fryer": ["air fryer", "fryer"],
    "purifiers": ["purifier", "water purifier", "air purifier"],
    "purifier": ["purifier", "water purifier", "air purifier"],
    
    # Watches & Extras
    "watches": ["watch", "smartwatch"],
    "watch": ["watch", "smartwatch"],
    "smartwatches": ["smartwatch", "watch"],
    "smartwatch": ["smartwatch", "watch"],
    "sunglasses": ["sunglasses", "shades"],
    "books": ["book", "paperback"],
    "book": ["book", "paperback"]
}

STOPWORDS = {
    "under", "below", "above", "over", "less", "than", "more", "greater",
    "within", "between", "from", "to", "and", "or", "for", "in", "with",
    "the", "a", "an", "at", "by", "of", "on", "is", "are", "best", "good",
    "top", "cheap", "all", "buy", "show", "get", "me", "find", "looking",
    "rs", "inr", "rupees", "rupee", "k", "thousand", "lakh", "lac",
    "price", "cost", "budget", "rate", "around", "nearby", "item", "items",
    "product", "products", "upto", "up"
}

def parse_price_value(val_str: str, unit: Optional[str] = None) -> float:
    try:
        val = float(val_str.replace(",", "").strip())
        if unit:
            u = unit.lower().strip()
            if u in ["k", "thousand"]:
                val *= 1000
            elif u in ["lakh", "lac"]:
                val *= 100000
        return val
    except Exception:
        return 0.0

def parse_natural_query(raw_query: str) -> Tuple[List[str], Optional[float], Optional[float]]:
    """
    Extracts search keywords, min_price, and max_price from natural language search queries.
    Examples:
      - "sarees under 500" -> (['saree', 'sari'], None, 500.0)
      - "laptops under 50000" -> (['laptop', 'notebook', ...], None, 50000.0)
      - "dress between 2000 and 5000" -> (['dress', 'gown', ...], 2000.0, 5000.0)
      - "nike running shoes" -> (['nike', 'running', 'shoe', ...], None, None)
    """
    if not raw_query:
        return [], None, None

    text = raw_query.lower().strip()
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    # 1. Price range: "between X and Y" / "from X to Y" / "X to Y"
    between_match = re.search(
        r'(?:between|from)?\s*(?:rs\.?|inr|₹)?\s*([0-9]+(?:\.[0-9]+)?)\s*(k|thousand|lakh|lac)?\s*(?:and|to|-)\s*(?:rs\.?|inr|₹)?\s*([0-9]+(?:\.[0-9]+)?)\s*(k|thousand|lakh|lac)?',
        text
    )
    if between_match and between_match.group(1) and between_match.group(3):
        p1 = parse_price_value(between_match.group(1), between_match.group(2))
        p2 = parse_price_value(between_match.group(3), between_match.group(4))
        if p1 > 0 and p2 > 0:
            min_price = min(p1, p2)
            max_price = max(p1, p2)
            text = text[:between_match.start()] + " " + text[between_match.end():]

    # 2. Maximum price: "under / below / less than / within / max / <= / < / upto / up to X"
    if max_price is None:
        under_match = re.search(
            r'(?:under|below|less\s+than|within|max|<=|<|upto|up\s+to)\s*(?:rs\.?|inr|₹)?\s*([0-9]+(?:\.[0-9]+)?)\s*(k|thousand|lakh|lac)?',
            text
        )
        if under_match:
            max_price = parse_price_value(under_match.group(1), under_match.group(2))
            text = text[:under_match.start()] + " " + text[under_match.end():]

    # 2b. Trailing maximum price: "X and below / X or less / X under / X below"
    if max_price is None:
        trailing_max = re.search(
            r'(?:rs\.?|inr|₹)?\s*([0-9]+(?:\.[0-9]+)?)\s*(k|thousand|lakh|lac)?\s*(?:and\s+below|or\s+less|under|below)',
            text
        )
        if trailing_max:
            max_price = parse_price_value(trailing_max.group(1), trailing_max.group(2))
            text = text[:trailing_max.start()] + " " + text[trailing_max.end():]

    # 3. Minimum price: "above / over / more than / greater than / min / >= / > X"
    if min_price is None:
        above_match = re.search(
            r'(?:above|over|more\s+than|greater\s+than|min|>=|>)\s*(?:rs\.?|inr|₹)?\s*([0-9]+(?:\.[0-9]+)?)\s*(k|thousand|lakh|lac)?',
            text
        )
        if above_match:
            min_price = parse_price_value(above_match.group(1), above_match.group(2))
            text = text[:above_match.start()] + " " + text[above_match.end():]

    # 3b. Trailing minimum price: "X and above / X or more"
    if min_price is None:
        trailing_min = re.search(
            r'(?:rs\.?|inr|₹)?\s*([0-9]+(?:\.[0-9]+)?)\s*(k|thousand|lakh|lac)?\s*(?:and\s+above|or\s+more)',
            text
        )
        if trailing_min:
            min_price = parse_price_value(trailing_min.group(1), trailing_min.group(2))
            text = text[:trailing_min.start()] + " " + text[trailing_min.end():]

    # 4. Tokenize remaining words
    raw_tokens = re.findall(r'[a-zA-Z0-9]+', text)
    primary_keywords: List[str] = []
    expanded_keywords: List[str] = []

    for token in raw_tokens:
        tok = token.lower().strip()
        if tok.isdigit():
            continue

        if tok in STOPWORDS or len(tok) < 2:
            continue

        if tok not in primary_keywords:
            primary_keywords.append(tok)

        # Look up synonyms & stems
        syns = SYNONYMS_AND_STEMS.get(tok, [tok])
        for s in syns:
            if s not in expanded_keywords:
                expanded_keywords.append(s)

    # Combine primary first, then expanded
    final_keywords = primary_keywords.copy()
    for exp in expanded_keywords:
        if exp not in final_keywords:
            final_keywords.append(exp)

    return final_keywords, min_price, max_price

def search_products(
    db: Session,
    raw_query: Optional[str] = None,
    category_id: Optional[int] = None,
    subcategory: Optional[str] = None,
    skip: int = 0,
    limit: int = 300
) -> List[Product]:
    """
    Intelligent product search with natural language parsing, STRICT price filtering,
    and relevance scoring.
    """
    query = db.query(Product)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if subcategory:
        query = query.filter(Product.subcategory.ilike(f"%{subcategory}%"))

    if not raw_query or not raw_query.strip():
        return query.offset(skip).limit(limit).all()

    keywords, min_price, max_price = parse_natural_query(raw_query)

    all_candidates = query.all()

    if not keywords and max_price is None and min_price is None:
        return all_candidates[skip : skip + limit]

    scored_items: List[Tuple[float, float, Product]] = []

    for p in all_candidates:
        # STRICT price check: Never return items violating user's price criteria
        if min_price is not None and p.price < min_price:
            continue
        if max_price is not None and p.price > max_price:
            continue

        score = 0.0
        p_name = (p.name or "").lower()
        p_brand = (p.brand or "").lower()
        p_desc = (p.description or "").lower()
        p_subcat = (p.subcategory or "").lower()
        p_cat = (p.category.name if p.category else "").lower()
        p_specs = (p.specifications or "").lower()

        # If user searched specific keywords
        if keywords:
            for kw in keywords:
                kw_lower = kw.lower()
                # Exact word or substring matches
                if kw_lower in p_name:
                    score += 25.0
                    if p_name.startswith(kw_lower) or f" {kw_lower}" in p_name:
                        score += 10.0
                if kw_lower in p_subcat:
                    score += 18.0
                if kw_lower in p_brand:
                    score += 15.0
                if kw_lower in p_cat:
                    score += 12.0
                if kw_lower in p_desc:
                    score += 6.0
                if kw_lower in p_specs:
                    score += 4.0
        else:
            # Only price filtering requested (e.g. "under 500")
            score = 10.0

        # If item has a relevance match (or purely price search)
        if score > 0:
            scored_items.append((score, p.price, p))

    if scored_items:
        # Sort by relevance score desc, then price asc
        scored_items.sort(key=lambda item: (-item[0], item[1]))
        return [item[2] for item in scored_items][skip : skip + limit]

    return []

