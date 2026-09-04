import random
import json
import os
import sys
from datetime import datetime, timedelta

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal, engine, Base
from models.category import Category
from models.product import Product
from models.user import User
from models.review import Review
from models.price_history import PriceHistory

def seed_database():
    print("Re-creating all database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    
    print("Seeding Categories...")
    category_list = [
        {"name": "Women's Fashion", "desc": "All ethnic, western, sarees, dresses, chudidhars, jeans, frocks, and luxury bags for women"},
        {"name": "Home Appliances", "desc": "Smart Refrigerators, Washing Machines, Air Fryers, Microwaves, ACs and Kitchenware"},
        {"name": "Men's Fashion", "desc": "Formal Suits, Denim Shirts, Polos, Hoodies, and Trousers"},
        {"name": "Footwear", "desc": "Running Shoes, Sneakers, Formal Loafers, Heels, and Sandals"},
        {"name": "Electronics", "desc": "Laptops, Smartphones, Noise-Cancelling Headphones, and Smart Gadgets"},
        {"name": "Beauty & Grooming", "desc": "Luxury Perfumes, Skincare Serums, Makeup, and Styling Appliances"},
        {"name": "Watches & Accessories", "desc": "Luxury Watches, Chronographs, Polarized Sunglasses, and Leather Wallets"},
        {"name": "Kids & Toys", "desc": "Children's Clothing, LEGO Star Wars, RC Cars, and Toys"},
        {"name": "Sports & Fitness", "desc": "Badminton Racquets, Yoga Mats, Activewear, and Fitness Gear"},
        {"name": "Books", "desc": "Bestselling Non-Fiction, Self-Help, and Fiction Masterpieces"}
    ]
    
    category_map = {}
    for c_info in category_list:
        cat = Category(name=c_info["name"], description=c_info["desc"])
        db.add(cat)
        db.flush()
        category_map[c_info["name"]] = cat.id

    db.commit()

    print("Seeding Rich Catalog with all Women's Fashion items (20 Sarees, 20 Dresses, 20 Chudidhars, Jeans, Frocks, Handbags) & Home Appliances...")
    
    products_data = [
        # =========================================================================
        # --- WOMEN'S FASHION: 1. SAREES (20 Items) ---
        # =========================================================================
        {
            "name": "Kanjivaram Pure Silk Gold Zari Bridal Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Nalli Silks",
            "price": 14999.0,
            "discount": 15.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Authentic crimson red Kanjivaram pure silk saree handwoven with pure gold electroplated zari motifs and heavy pallu. Comes with unstitched blouse piece.",
            "specs": {"Fabric": "100% Pure Mulberry Silk", "Zari": "Gold Electroplated Zari", "Occasion": "Bridal / Wedding", "Length": "5.5m + 0.8m Blouse", "Care": "Dry Clean Only"}
        },
        {
            "name": "Royal Banarasi Brocade Art Silk Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "FabIndia",
            "price": 6490.0,
            "discount": 20.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Exquisite Banarasi woven saree featuring intricate floral jaal weaving and contrast emerald green border for grand celebrations.",
            "specs": {"Fabric": "Banarasi Art Silk", "Weave Type": "Jacquard Brocade", "Border": "Contrast Zari Border", "Length": "6.3 Meters with Blouse", "Care": "Dry Clean"}
        },
        {
            "name": "Pastel Pink Chanderi Handloom Floral Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Biba",
            "price": 4299.0,
            "discount": 25.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Lightweight breathable Chanderi silk cotton saree with pastel hand-block floral print and delicate gold tissue border.",
            "specs": {"Fabric": "Chanderi Silk Cotton", "Print": "Hand-block Floral", "Transparency": "Semi-Sheer", "Length": "5.5 Meters", "Blouse": "Unstitched Cotton Silk 0.8m"}
        },
        {
            "name": "Soft Georgette Party Wear Sequin Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Sabyasachi Heritage",
            "price": 8990.0,
            "discount": 10.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Midnight blue flowing georgette saree embellished with tone-on-tone shimmering micro sequins. Lightweight and effortlessly glamorous for cocktail nights.",
            "specs": {"Fabric": "Pure Georgette", "Work": "Micro Sequin Embroidery", "Occasion": "Cocktail / Reception", "Drape": "Fluid Fall"}
        },
        {
            "name": "Organza Floral Printed Pastel Mint Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Kalki Fashion",
            "price": 5490.0,
            "discount": 30.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Ultra-fine sheer organza saree with digital watercolor peony prints and hand-cut scalloped embroidered borders.",
            "specs": {"Fabric": "Premium Organza", "Border": "Scalloped Cutwork", "Pattern": "Digital Watercolor Print", "Length": "5.5m"}
        },
        {
            "name": "Pure Chiffon Ombre Dual-Tone Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Manyavar Mohey",
            "price": 3799.0,
            "discount": 15.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Featherlight pure chiffon saree featuring dual-tone ombre sunset shades and delicate metallic gota patti lace.",
            "specs": {"Fabric": "Pure Chiffon", "Type": "Ombre Shaded", "Border": "Gota Patti Lace", "Wash Care": "Hand Wash Mild"}
        },
        {
            "name": "Traditional Bandhani Jaipuri Silk Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Meena Bazaar",
            "price": 4999.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Authentic Rajasthani tie-and-dye Bandhej silk saree in vibrant scarlet and mustard with traditional broad mirror-work border.",
            "specs": {"Fabric": "Art Silk Bandhej", "Craft": "Authentic Tie & Dye", "Origin": "Jaipur, Rajasthan", "Weight": "450g"}
        },
        {
            "name": "Mysore Crepe Silk Gold Zari Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "KSIC Mysore Silk",
            "price": 11990.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Original Mysore crepe silk with rich smooth texture, pure zari border, and hallmark silk guarantee tag.",
            "specs": {"Fabric": "Pure Crepe Silk 100%", "Certification": "Silk Mark Certified", "Zari": "Pure Gold & Silver Thread", "Care": "Dry Clean"}
        },
        {
            "name": "Kerala Kasavu Traditional Off-White Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "FabIndia",
            "price": 2890.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Traditional Onam festive cotton-tissue Kasavu saree in off-white cream with broad woven golden temple borders.",
            "specs": {"Fabric": "Fine Combed Cotton & Tissue", "Occasion": "Festive / Traditional", "Border": "Golden Temple Kasavu", "Length": "6.25m"}
        },
        {
            "name": "Maharashtrian Paithani Silk Peacock Motif Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Yeola Paithani",
            "price": 13490.0,
            "discount": 12.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Handcrafted royal Yeola Paithani saree in magenta featuring traditional mor-bangadi (peacock in bangle) woven pallu.",
            "specs": {"Fabric": "Pure Handloom Paithani Silk", "Pallu Motif": "Peacock Tapestry Weave", "Origin": "Yeola, Maharashtra", "Care": "Dry Clean"}
        },
        {
            "name": "Hand-painted Tussar Silk Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Craftsvilla",
            "price": 6890.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Wild Tussar raw silk saree adorned with authentic Madhubani hand-painted tree-of-life folklore artwork on natural beige ground.",
            "specs": {"Fabric": "100% Wild Tussar Silk", "Art": "Hand-Painted Madhubani", "Texture": "Rich Raw Textured", "Length": "5.5m"}
        },
        {
            "name": "Patan Patola Double Ikat Silk Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Heritage Weaves",
            "price": 16990.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Masterpiece geometric double Ikat Patola silk saree with natural resist-dye colors, reversible identical patterns on both sides.",
            "specs": {"Fabric": "Pure Mulberry Patola Silk", "Weave": "Double Ikat Geometric", "Dyeing": "Natural Eco Dyes", "Care": "Dry Clean"}
        },
        {
            "name": "Kalamkari Handblock Printed Organic Cotton Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "FabIndia",
            "price": 2790.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Eco-friendly natural vegetable dyed Srikalahasti Kalamkari cotton saree with mythological artwork and floral creepers.",
            "specs": {"Fabric": "100% Organic Soft Cotton", "Craft": "Pen Kalamkari Block Print", "Dyes": "Natural Plant Dyes", "Length": "5.5m + Blouse"}
        },
        {
            "name": "Pochampally Ikat Handloom Silk Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Pochampally Weavers",
            "price": 7990.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Telangana GI-tagged Pochampally silk saree featuring distinctive diamond Ikat waves and contrast golden zari temple borders.",
            "specs": {"Fabric": "Pure Pochampally Silk", "Weave": "Single Ikat Precision Weave", "GI Tagged": "Yes", "Length": "6.3m"}
        },
        {
            "name": "100% Pure Organic Linen Summer Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Anokhi",
            "price": 3990.0,
            "discount": 25.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Breathable 100 count pure European flax linen saree in sage green with silver zari pinstripes and handmade thread tassels.",
            "specs": {"Fabric": "100% Organic European Flax Linen", "Count": "100 Count Fine Linen", "Pallu": "Handcrafted Tassels", "Care": "Gentle Wash"}
        },
        {
            "name": "Bengal Handloom Tant Cotton Jamdani Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Biswa Bangla",
            "price": 2490.0,
            "discount": 18.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Crisp airy Dhaniakhali Bengal cotton saree with intricate Jamdani buta weaving across the body. The quintessential summer favorite.",
            "specs": {"Fabric": "100% Combed Bengal Tant Cotton", "Weave": "Jamdani Floral Buta", "Origin": "West Bengal", "Length": "5.5m"}
        },
        {
            "name": "Royal Velvet Heavy Embroidered Zardozi Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Tarun Tahiliani",
            "price": 18990.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Deep wine micro-velvet luxury saree adorned with antique zardozi hand embroidery, pearl drops, and rich velvet blouse.",
            "specs": {"Fabric": "Micro Velvet & Net Pleats", "Embroidery": "Hand Zardozi & Dabka Work", "Occasion": "Winter Wedding", "Blouse": "Stitched Designer 38-42"}
        },
        {
            "name": "Metallic Gold Shimmer Tissue Silk Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Manish Malhotra",
            "price": 12490.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Glossy high-shine champagne gold tissue silk saree as seen on celebrities. Ultra-glamorous, sleek, and feather-light.",
            "specs": {"Fabric": "Tissue Silk Metallic Blend", "Finish": "High-Gloss Champagne Sheen", "Occasion": "Red Carpet / Sangeet", "Length": "5.5m"}
        },
        {
            "name": "Ready-to-Wear Ruffle Pleated Georgette Saree",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Kalki Fashion",
            "price": 4690.0,
            "discount": 30.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Pre-stitched 1-minute ruffle saree with pre-formed pleats and matching embroidered designer belt. No draping hassle required.",
            "specs": {"Fabric": "Flowing Georgette with Tiered Ruffles", "Style": "1-Minute Ready to Wear", "Includes": "Embroidered Buckle Belt + Blouse", "Size": "Adjustable Waist 28-38"}
        },
        {
            "name": "Heavy Satin Crepe Cocktail Saree with Stone Work",
            "category": "Women's Fashion",
            "subcategory": "Sarees",
            "brand": "Biba",
            "price": 5290.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Silky smooth heavy satin crepe saree in emerald green with Swarovski rhinestone studded borders and contrast satin blouse.",
            "specs": {"Fabric": "Premium Heavy Satin Crepe", "Work": "Swarovski Crystal Borders", "Drape": "Heavy Falling Silhouette", "Length": "5.5m + 0.8m"}
        },

        # =========================================================================
        # --- WOMEN'S FASHION: 2. DRESSES (20 Items) ---
        # =========================================================================
        {
            "name": "Women's Floral Print Tiered Maxi Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Zara",
            "price": 3490.0,
            "discount": 15.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Breezy bohemian floral summer maxi dress crafted from breathable rayon. Features ruffled tiers and adjustable spaghetti straps.",
            "specs": {"Fabric": "100% Rayon Viscose", "Length": "Ankle-Length Maxi", "Pattern": "Botanical Floral", "Fit": "Flowy Relaxed"}
        },
        {
            "name": "Royal Emerald Velvet Bodycon Cocktail Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Mango",
            "price": 4990.0,
            "discount": 20.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Luxe stretch velvet sheath dress in rich emerald green with a flattering sweetheart neckline and side slit.",
            "specs": {"Fabric": "92% Polyester, 8% Elastane Velvet", "Fit": "Bodycon Slim", "Neckline": "Sweetheart Neck", "Closure": "Concealed Back Zip"}
        },
        {
            "name": "French Lace A-Line Fit & Flare Party Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Forever New",
            "price": 5990.0,
            "discount": 25.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80"],
            "description": "Delicate guipure floral lace mini dress with cap sleeves, structured sweetheart bustier, and flared skater skirt.",
            "specs": {"Fabric": "Embroidered Guipure Lace & Satin Lining", "Silhouette": "Fit & Flare", "Length": "Above Knee", "Color": "Blush Rose"}
        },
        {
            "name": "Bohemian Tiered Smock Midi Summer Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "H&M",
            "price": 2299.0,
            "discount": 30.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80"],
            "description": "Relaxed cotton poplin midi dress with puff balloon sleeves, tiered gathered skirt, and tassel keyhole neckline.",
            "specs": {"Material": "100% Pure Cotton Poplin", "Sleeves": "Puff Balloon Sleeves", "Length": "Midi Calf-Length", "Wash": "Machine Wash Cold"}
        },
        {
            "name": "Silk Satin Cowl Neck Slip Evening Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Zara",
            "price": 3990.0,
            "discount": 10.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80"],
            "description": "90s vintage inspired satin slip dress featuring fluid cowl drape neck, low back with crisscross straps, and high leg slit.",
            "specs": {"Fabric": "Silk-Touch Poly Satin", "Neckline": "Cowl Drape", "Back": "Open Crisscross Lace-up", "Length": "Maxi"}
        },
        {
            "name": "Classic Vintage Polka Dot Retro Swing Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Marks & Spencer",
            "price": 3290.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80"],
            "description": "Iconic Audrey-style polka dot swing dress in monochrome black and white with waist cinch belt and side pockets.",
            "specs": {"Material": "97% Cotton, 3% Spandex Stretch", "Pattern": "Vintage Polka Dot", "Includes": "Matching Fabric Belt", "Pockets": "2 Functional"}
        },
        {
            "name": "Denim Belted Button-Down Shirt Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Levi's",
            "price": 3799.0,
            "discount": 25.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80"],
            "description": "Medium indigo wash 100% cotton denim shirt dress with chest flap pockets, point collar, and tie-around waist belt.",
            "specs": {"Material": "100% Cotton Denim", "Closure": "Metallic Snap Buttons", "Fit": "Structured A-Line", "Sleeves": "Roll-up Long Sleeves"}
        },
        {
            "name": "Off-Shoulder Mermaid Evening Ball Gown",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Forever New",
            "price": 8490.0,
            "discount": 15.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80"],
            "description": "Sculpting crepe off-shoulder evening gown with boned corset bodice and dramatic fishtail mermaid flare train.",
            "specs": {"Fabric": "Bonded Heavy Crepe", "Style": "Mermaid Trumpet Gown", "Neckline": "Off-The-Shoulder Foldover", "Occasion": "Gala / Black Tie"}
        },
        {
            "name": "Ribbed Knit Bodycon Sweater Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "MANGO",
            "price": 3290.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80"],
            "description": "Warm and cozy ribbed knit midi sweater dress with high turtleneck and figure-hugging stretch knit silhouette.",
            "specs": {"Material": "60% Viscose, 40% Polyamide Knit", "Neckline": "Turtleneck", "Length": "Midi", "Warmth": "Autumn / Winter Cozy"}
        },
        {
            "name": "Pleated Chiffon Tiered Cocktail Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "ONLY",
            "price": 2790.0,
            "discount": 30.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80"],
            "description": "Sunburst pleated chiffon knee-length dress in pastel lilac with sheer flutter sleeves and elasticated cinched waist.",
            "specs": {"Fabric": "Accordion Pleated Chiffon", "Sleeves": "Flutter Sheer Sleeves", "Color": "Pastel Lilac", "Lining": "Full Soft Tricot"}
        },
        {
            "name": "Pure Linen Wrap Midi Dress with Pocket",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "FabIndia",
            "price": 3690.0,
            "discount": 15.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80"],
            "description": "Natural breathable linen wrap dress with side tie fastening, deep V-neck, and practical patch pockets.",
            "specs": {"Fabric": "100% Pure Flax Linen", "Style": "True Wrap Dress", "Closure": "Self-tie Belt", "Pocket": "Dual Patch Pockets"}
        },
        {
            "name": "Tailored Double-Breasted Tuxedo Blazer Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Zara",
            "price": 5490.0,
            "discount": 10.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80"],
            "description": "Power-dressing mini blazer dress featuring peak satin lapels, padded shoulders, and engraved double-breasted buttons.",
            "specs": {"Material": "Poly-Viscose Suiting Crepe", "Fit": "Structured Slim", "Buttons": "Gold Metal Crest Buttons", "Lapel": "Satin Peak Lapel"}
        },
        {
            "name": "Halter Neck Printed Tropical Sundress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "H&M",
            "price": 1999.0,
            "discount": 35.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80"],
            "description": "Vibrant palm leaf print vacation sundress with halter neck tie, backless cutout, and tiered ruffled hem.",
            "specs": {"Fabric": "100% Viscose", "Neckline": "Halter Tie", "Back": "Low Cutout Back", "Occasion": "Beach / Resort Vacation"}
        },
        {
            "name": "Metallic Gold Sequin Party Mini Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Forever 21",
            "price": 3890.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80"],
            "description": "All-over sparkling liquid gold sequins on stretch mesh with long sleeves and deep plunge back for New Year celebrations.",
            "specs": {"Fabric": "Sequined Mesh with Soft Jersey Lining", "Length": "Mini", "Sleeves": "Full Long Sleeves", "Shine": "High Reflection"}
        },
        {
            "name": "Embroidered Cottagecore White Prairie Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Urbanic",
            "price": 2890.0,
            "discount": 25.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80"],
            "description": "Romantic milkmaid prairie dress in white eyelet schiffli cotton with square neckline and ruffled cap sleeves.",
            "specs": {"Fabric": "100% Schiffli Embroidered Cotton", "Neckline": "Square Milkmaid Neck", "Color": "Crisp Optical White", "Length": "Midi"}
        },
        {
            "name": "Silk Kaftan Bohemian Resort Maxi Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Ritu Kumar",
            "price": 6490.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80"],
            "description": "Flowy printed silk blend kaftan dress with beaded drawstring waistband and side slits. Epitome of effortless resort luxury.",
            "specs": {"Fabric": "Silk Poly Georgette", "Fit": "Oversized Fluid Kaftan", "Details": "Handmade Beaded Tassels", "Size": "Free Size (Fits S-XXL)"}
        },
        {
            "name": "Ruched Asymmetric Satin Midi Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "MANGO",
            "price": 4290.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80"],
            "description": "Sculpting satin dress featuring all-over side ruching, one-shoulder neckline, and asymmetrical handkerchief hemline.",
            "specs": {"Fabric": "Stretch Heavy Satin", "Hemline": "Asymmetrical Drape", "Neck": "One Shoulder", "Color": "Deep Wine"}
        },
        {
            "name": "Tiered Puff Sleeve Organza Cocktail Frock",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Forever New",
            "price": 5790.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=700&auto=format&fit=crop&q=80"],
            "description": "Voluminous floral organza party frock with dramatic oversized puff sleeves, fitted waistline, and flared mini skirt.",
            "specs": {"Fabric": "Structured Printed Organza", "Sleeves": "Statement Puff Sleeves", "Length": "Mini 34 inches", "Lining": "Opaque Satin"}
        },
        {
            "name": "Minimalist High-Neck Sleeveless Column Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Massimo Dutti",
            "price": 6990.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=700&auto=format&fit=crop&q=80"],
            "description": "Understated quiet-luxury column maxi dress in black crepe jersey with high mock neck and clean back zipper line.",
            "specs": {"Fabric": "Heavy Italian Stretch Crepe", "Cut": "Straight Column Silhouette", "Neck": "Mock High Neck", "Length": "Floor Length"}
        },
        {
            "name": "Cutout Waist Broderie Anglaise Summer Dress",
            "category": "Women's Fashion",
            "subcategory": "Dresses & Gowns",
            "brand": "Zara",
            "price": 3690.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=700&auto=format&fit=crop&q=80"],
            "description": "Terracotta embroidered cotton sundress featuring subtle waist side cutouts, ring front detail, and flowy midi skirt.",
            "specs": {"Fabric": "100% Broderie Anglaise Cotton", "Details": "Waist Ring Cutout", "Color": "Terracotta Clay", "Care": "Machine Wash"}
        },

        # =========================================================================
        # --- WOMEN'S FASHION: 3. CHUDIDHARS & SUITS (20 Items) ---
        # =========================================================================
        {
            "name": "Royal Anarkali Heavy Embroidered Kurti & Churidar Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Biba",
            "price": 4890.0,
            "discount": 25.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Floor-length flared Anarkali suit in pure cotton with zari thread embroidery, matching stretchy churidar bottoms, and embellished chiffon dupatta.",
            "specs": {"Fabric": "100% Premium Cotton", "Set Includes": "Anarkali Kurti, Churidar, Dupatta", "Pattern": "Zari Thread Embroidered", "Sleeve": "3/4th Sleeve"}
        },
        {
            "name": "Pure Chanderi Silk Straight Cut Churidar Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "FabIndia",
            "price": 5490.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Regal bottle green Chanderi silk straight kurta featuring golden zari work, paired with pure silk churidar and woven Banarasi dupatta.",
            "specs": {"Fabric": "Pure Chanderi Silk", "Bottom Type": "Gathered Churidar", "Dupatta": "Banarasi Woven Silk", "Care": "Dry Clean"}
        },
        {
            "name": "Pakistani Style Lawn Cotton Printed Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Gul Ahmed",
            "price": 3490.0,
            "discount": 15.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Luxurious soft lawn cotton printed long kameez with organza embroidered daman border, paired with cigarette pants and silk dupatta.",
            "specs": {"Fabric": "100% Swiss Lawn Cotton", "Embellishment": "Organza Patchwork Daman", "Bottom": "Cotton Cigarette Pants", "Dupatta": "Digital Silk 2.5m"}
        },
        {
            "name": "Georgette Flared Sharara Suit with Mirror Work",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Kalki Fashion",
            "price": 6990.0,
            "discount": 30.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Mustard yellow short peplum kurti adorned with real mirror work and gota lace, paired with voluminous tiered flared sharara pants.",
            "specs": {"Fabric": "Pure Georgette with Shantoon Lining", "Work": "Real Glass Mirror Work", "Sharara Flare": "3.5m Flared Leg", "Occasion": "Haldi / Sangeet"}
        },
        {
            "name": "Velvet Winter Embroidered Kurti & Churidar Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Manyavar Mohey",
            "price": 7890.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Deep maroon plush micro velvet straight kurta featuring intricate Kashmiri Tilla embroidery, paired with velvet churidar and warm Pashmina stole.",
            "specs": {"Fabric": "Plush Micro Velvet 9000", "Embroidery": "Kashmiri Tilla Handwork", "Includes": "Kurti, Churidar, Pashmina Stole", "Season": "Winter Festive"}
        },
        {
            "name": "Lucknowi Chikankari Hand Embroidered Kurta Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Ada Chikankari",
            "price": 4290.0,
            "discount": 20.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Hand-embroidered pure georgette kurta featuring Bakhiya and Phanda Chikankari stitches with Mukaish work, matching slip, and churidar.",
            "specs": {"Fabric": "Viscose Georgette", "Craft": "Authentic Lucknowi Hand Chikankari", "Stitches": "Bakhiya, Phanda & Mukaish", "Includes": "Matching Inner Slip"}
        },
        {
            "name": "Banarasi Brocade Silk Salwar Kameez Suit",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Meena Bazaar",
            "price": 8490.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Rich royal blue Banarasi katan silk kurta with gold woven floral motifs, paired with pure raw silk churidar and heavy tissue dupatta.",
            "specs": {"Fabric": "Pure Banarasi Katan Silk", "Weave": "Kadwa Zari Brocade", "Bottom": "Raw Silk Stitched Churidar", "Care": "Dry Clean"}
        },
        {
            "name": "Festive Mughal Angrakha Style Flared Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "W for Woman",
            "price": 3890.0,
            "discount": 25.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Mughal crossover Angrakha flared kurta with side tassel tie-up, paired with stretch churidar pants and foil printed net dupatta.",
            "specs": {"Fabric": "Cotton Silk Blend", "Style": "Angrakha Crossover", "Tassels": "Handmade Latkans", "Sleeves": "Full Churidar Sleeves"}
        },
        {
            "name": "Daily Wear Floral Printed Pure Cotton Churidar Suit",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Aurelia",
            "price": 1999.0,
            "discount": 30.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Ultra-soft 60s combed cotton everyday straight kurta with blooming floral print, paired with breathable cotton churidar and chiffon dupatta.",
            "specs": {"Fabric": "100% Breathable Combed Cotton", "Comfort": "All-Day Office & Home Wear", "Bottom": "Elasticated Cotton Churidar", "Wash": "Machine Wash"}
        },
        {
            "name": "Rajasthani Mirror Work Kurta & Palazzo Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Global Desi",
            "price": 3290.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Contemporary mustard ethnic A-line kurta featuring mirror and thread yoke embroidery, paired with wide-leg printed palazzo pants.",
            "specs": {"Fabric": "Rayon Crepe Blend", "Embroidery": "Folk Mirror Work Yoke", "Bottom": "Wide Leg Flared Palazzo", "Fit": "Regular Comfort"}
        },
        {
            "name": "Traditional Punjabi Patiala Salwar Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Soch",
            "price": 3690.0,
            "discount": 25.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Vibrant emerald green short kurta with Phulkari embroidered neckline, paired with full heavy-pleat Punjabi Patiala salwar and Phulkari dupatta.",
            "specs": {"Fabric": "Glazed Cotton & Chiffon", "Salwar Style": "Full Pleated Heavy Patiala", "Dupatta": "Traditional Amritsari Phulkari", "Care": "Hand Wash"}
        },
        {
            "name": "Designer Jacquard Silk Party Kurti & Churidar Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Biba",
            "price": 4590.0,
            "discount": 15.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Rich wine jacquard weave straight kurta with mandarin collar and metallic buttons, paired with matching stretch churidar pants.",
            "specs": {"Fabric": "Silk Jacquard Blend", "Collar": "Mandarin Collar with Placket", "Lining": "Soft Cotton Shantoon", "Bottom": "Lycra Stretch Churidar"}
        },
        {
            "name": "Pastel Mint Organza Thread Work Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Kalki Fashion",
            "price": 6290.0,
            "discount": 20.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Dreamy pastel mint sheer organza kurta with delicate silk thread embroidery, paired with cotton satin cigarette pants and scalloped dupatta.",
            "specs": {"Fabric": "Premium Organza & Satin", "Embroidery": "Tone-on-Tone Silk Thread", "Dupatta": "Scalloped Organza 2.4m", "Occasion": "Day Wedding / Engagement"}
        },
        {
            "name": "Zari Embroidered Festive Silk Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "FabIndia",
            "price": 5990.0,
            "discount": 10.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Heritage raw silk straight kurta in royal purple adorned with authentic antique zari embroidery on sleeves and neckline with matching churidar.",
            "specs": {"Fabric": "Pure Raw Silk 100%", "Work": "Antique Zari & Sequin", "Bottom": "Fitted Raw Silk Churidar", "Care": "Dry Clean Only"}
        },
        {
            "name": "Indo-Western Fusion Crop Top & Sharara Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Global Desi",
            "price": 4190.0,
            "discount": 25.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Embroidered padded sweetheart crop top paired with pleated flared sharara pants and a dramatic floor-sweeping cape jacket.",
            "specs": {"Fabric": "Georgette with Foil Print", "Style": "Crop Top, Sharara & Cape", "Closure": "Side Zip & Elastic Waist", "Occasion": "Festive / Sangeet"}
        },
        {
            "name": "Traditional Bandhani Print Silk Salwar Suit",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Meena Bazaar",
            "price": 3590.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Jaipuri red and yellow Bandhej printed silk kurta with gota patti work on neck, paired with solid churidar and pure chiffon bandhani dupatta.",
            "specs": {"Fabric": "Art Silk Bandhej", "Craft": "Rajasthani Bandhej Print", "Bottom": "Cotton Lycra Churidar", "Includes": "Kurta, Churidar, Dupatta"}
        },
        {
            "name": "Chanderi Silk Flared Gharara Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "W for Woman",
            "price": 4990.0,
            "discount": 20.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
            "description": "Powder pink short Chanderi kurta with gotta embroidery, paired with voluminous two-tier flared gharara bottoms and net dupatta.",
            "specs": {"Fabric": "Pure Chanderi Silk & Cotton Lining", "Bottom": "Two-Tier Flared Gharara", "Color": "Pastel Powder Pink", "Care": "Dry Clean"}
        },
        {
            "name": "Handblock Printed Indigo Cotton Churidar Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "FabIndia",
            "price": 2690.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
            "description": "Authentic natural indigo Dabu mud-resist handblock printed straight cotton kurta with matching navy churidar and Kota Doria dupatta.",
            "specs": {"Fabric": "100% Handloom Cotton", "Print": "Indigo Dabu Block Print", "Dupatta": "Kota Doria Handloom", "Wash": "Hand Wash Cold"}
        },
        {
            "name": "High-Slit Straight Kurta with Cigarette Pants",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Aurelia",
            "price": 2490.0,
            "discount": 30.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
            "description": "Modern side high-slit straight kurta in navy with metallic floral foil print, paired with tailored ankle-length cigarette pants.",
            "specs": {"Fabric": "Poly Silk Crepe", "Slit": "Thigh-High Side Slits", "Bottom": "Tailored Cigarette Pants with Pockets", "Fit": "Slim Straight"}
        },
        {
            "name": "Gotta Patti Festive Chiffon Suit Set",
            "category": "Women's Fashion",
            "subcategory": "Chudidhars & Suits",
            "brand": "Soch",
            "price": 3990.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
            "description": "Vibrant peach flowing chiffon flared kurta adorned with traditional Jaipur gotta patti work on yoke and hem with matching churidar.",
            "specs": {"Fabric": "Pure Viscose Chiffon", "Work": "Handmade Gota Patti Work", "Bottom": "Cotton Lycra Gathered Churidar", "Occasion": "Festive / Puja"}
        },

        # =========================================================================
        # --- WOMEN'S FASHION: 4. JEANS, FROCKS, TOPS & BAGS ---
        # =========================================================================
        {
            "name": "Women's High-Rise Slim Stretch Denim Jeans",
            "category": "Women's Fashion",
            "subcategory": "Jeans & Bottoms",
            "brand": "Levi's",
            "price": 2799.0,
            "discount": 25.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=700&auto=format&fit=crop&q=80"],
            "description": "Classic high-waist stretchable denim jeans sculpting silhouette with all-day flexibility and shape retention.",
            "specs": {"Material": "98% Cotton, 2% Elastane", "Fit": "Slim Skinny Fit", "Rise": "High Rise"}
        },
        {
            "name": "Women's Wide-Leg Flared Vintage Denim Jeans",
            "category": "Women's Fashion",
            "subcategory": "Jeans & Bottoms",
            "brand": "Zara",
            "price": 3290.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=700&auto=format&fit=crop&q=80"],
            "description": "70s inspired relaxed wide-leg flare jeans in light stonewash with raw frayed hem.",
            "specs": {"Material": "100% Rigid Denim", "Fit": "Wide Leg Flare", "Rise": "Super High Rise"}
        },
        {
            "name": "Women's Ruffled Princess Party Frock Top",
            "category": "Women's Fashion",
            "subcategory": "Frocks & Tops",
            "brand": "Forever New",
            "price": 2990.0,
            "discount": 15.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=700&auto=format&fit=crop&q=80"],
            "description": "Chic flared organza party frock top with tiered ruffle collar, balloon sleeves, and pearl buttons.",
            "specs": {"Fabric": "Sheer Organza & Soft Camisole", "Sleeves": "Puff Balloon", "Fit": "Babydoll Flare"}
        },
        {
            "name": "Women's Luxury Saffiano Leather Structured Tote Handbag",
            "category": "Women's Fashion",
            "subcategory": "Handbags & Bags",
            "brand": "Michael Kors",
            "price": 16990.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=700&auto=format&fit=crop&q=80"],
            "description": "Signature Saffiano leather tote with polished gold-tone hardware, spacious interior laptop compartment, and zipper closure.",
            "specs": {"Material": "100% Saffiano Leather", "Dimensions": "15 x 11 x 5.5 inches", "Pockets": "3 Internal, 1 Zipper"}
        },

        # =========================================================================
        # --- 2. HOME APPLIANCES (20 Items) ---
        # =========================================================================
        {
            "name": "Samsung 653L French Door Smart Refrigerator",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Samsung",
            "price": 89990.0,
            "discount": 18.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1584990347449-399a9b70b5ee?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Side-by-side smart French door convertible refrigerator with AI Inverter Compressor, Family Hub touchscreen, and Beverage Center with auto-fill pitcher.",
            "specs": {"Capacity": "653 Liters", "Energy Rating": "5 Star Inverter", "Smart Feature": "Wi-Fi AI Family Hub Screen", "Warranty": "20 Years Compressor Warranty"}
        },
        {
            "name": "LG 9kg AI Direct Drive Front Load Washing Machine",
            "category": "Home Appliances",
            "subcategory": "Laundry & Cleaning",
            "brand": "LG",
            "price": 38990.0,
            "discount": 22.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=700&auto=format&fit=crop&q=80",
            "images": [
                "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=700&auto=format&fit=crop&q=80",
                "https://images.unsplash.com/photo-1585515320310-259814833e62?w=700&auto=format&fit=crop&q=80"
            ],
            "description": "Intelligent front loader with AI DD fabric sensor, Steam+ anti-allergy technology, TurboWash 360 in 39 mins, and ThinQ Wi-Fi smart control.",
            "specs": {"Capacity": "9 kg", "RPM": "1400 RPM", "Technology": "AI Direct Drive with Steam Allergy Care", "Energy Rating": "5 Star 2024", "Warranty": "10 Years Motor"}
        },
        {
            "name": "Daikin 1.5 Ton 5-Star Inverter Split Air Conditioner",
            "category": "Home Appliances",
            "subcategory": "Cooling & Heating",
            "brand": "Daikin",
            "price": 44990.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=700&auto=format&fit=crop&q=80"],
            "description": "Triple display inverter AC with 3D airflow, PM 2.5 air purification filter, Dew Clean indoor coil technology, and 54°C high ambient cooling.",
            "specs": {"Capacity": "1.5 Ton", "Energy Rating": "5 Star (ISEER 5.2)", "Refrigerant": "Eco-Friendly R32", "Condenser": "100% Copper Coil", "Warranty": "10 Yrs Compressor"}
        },
        {
            "name": "Philips Digital Air Fryer XL 6.2L (Rapid Air)",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Philips",
            "price": 9995.0,
            "discount": 25.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=700&auto=format&fit=crop&q=80"],
            "description": "Patented starfish Rapid Air technology with 7 one-touch digital cooking presets. Fry, grill, bake, and roast with up to 90% less fat.",
            "specs": {"Capacity": "6.2 Liters (1.2kg)", "Power": "2000 Watts", "Presets": "7 Touch Presets", "Warranty": "2 Years Global Warranty"}
        },
        {
            "name": "Morphy Richards 28L Convection Microwave Oven",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Morphy Richards",
            "price": 13990.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=700&auto=format&fit=crop&q=80"],
            "description": "Multi-stage cooking microwave with motorized rotisserie for tandoori kebabs, baking, grilling, and 120 Indian auto-cook recipes.",
            "specs": {"Capacity": "28 Liters", "Cavity": "Stainless Steel Mirror Finish", "Programs": "120+ Auto Menus", "Includes": "Rotisserie, Baking Plate, Wire Rack"}
        },
        {
            "name": "De'Longhi Dedica Pump Espresso & Cappuccino Maker",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "De'Longhi",
            "price": 22490.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=700&auto=format&fit=crop&q=80"],
            "description": "Slim 15-bar professional pump espresso machine with Thermoblock heating, adjustable milk frother wand for silky latte art, and dual cup filter.",
            "specs": {"Pressure": "15 Bar Professional Italian Pump", "Body": "Full Matte Stainless Steel", "Width": "Ultra Slim 15cm", "Heating": "Fast 35-sec Thermoblock"}
        },
        {
            "name": "ECOVACS Deebot N8 Pro Robotic Vacuum & Mop",
            "category": "Home Appliances",
            "subcategory": "Laundry & Cleaning",
            "brand": "ECOVACS",
            "price": 28990.0,
            "discount": 30.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1558317374-067fb5f30001?w=700&auto=format&fit=crop&q=80"],
            "description": "TrueDetect 3D obstacle avoidance robot vacuum with 2600Pa suction power, OZMO electronic mopping, LiDAR laser room mapping, and Alexa voice control.",
            "specs": {"Suction Power": "2600 Pa", "Navigation": "dToF Laser LiDAR Mapping", "Battery": "110 Mins Runtime", "App Control": "Live Multi-Floor Mapping"}
        },
        {
            "name": "Bosch 14 Place Settings Freestanding Dishwasher",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Bosch",
            "price": 42990.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1584990347449-399a9b70b5ee?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1584990347449-399a9b70b5ee?w=700&auto=format&fit=crop&q=80"],
            "description": "Engineered specifically for Indian oily cookware (kadhai, pressure cookers). Features Intensive Kadhai 70°C hygiene wash and EcoSilence Drive motor.",
            "specs": {"Capacity": "14 Place Settings", "Programs": "6 Wash Programs (Intensive 70°C)", "Noise Level": "44 dB Whisper Quiet", "Water Consumption": "9.5L per cycle"}
        },
        {
            "name": "Dyson V12 Detect Slim Cordless Vacuum Cleaner",
            "category": "Home Appliances",
            "subcategory": "Laundry & Cleaning",
            "brand": "Dyson",
            "price": 49900.0,
            "discount": 8.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1558317374-067fb5f30001?w=700&auto=format&fit=crop&q=80"],
            "description": "Laser illumination precisely reveals invisible dust on hard floors. Acoustic piezo sensor counts dust particles, showing proof on LCD screen.",
            "specs": {"Suction Power": "150 AW", "Runtime": "Up to 60 Mins", "Weight": "Lightweight 2.2 kg", "Filtration": "99.99% Whole-machine HEPA"}
        },
        {
            "name": "Nutribullet Pro 900W High-Speed Personal Blender",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Nutribullet",
            "price": 5999.0,
            "discount": 20.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=700&auto=format&fit=crop&q=80"],
            "description": "High-torque 900-watt power base with stainless steel extractor blades to pulverize nuts, frozen fruits, greens, and ice into silky smoothies in seconds.",
            "specs": {"Power": "900 Watts Motor", "Cups": "1 Tall Cup (900ml) + 1 Short Cup (500ml)", "Blades": "Cyclonic Stainless Steel Extractor", "Dishwasher Safe": "Yes"}
        },
        {
            "name": "Kent Grand Plus RO+UV+UF+TDS Smart Water Purifier",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Kent",
            "price": 15490.0,
            "discount": 18.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=700&auto=format&fit=crop&q=80"],
            "description": "Multi-stage RO+UV+UF purification with in-tank UV LED disinfection and patented TDS control retaining essential natural minerals.",
            "specs": {"Purification Capacity": "20 Liters/Hour", "Storage Tank": "9 Liters", "Technology": "RO + UV + UF + TDS Controller", "Warranty": "1 Year + 3 Years Free Service"}
        },
        {
            "name": "Sony Bravia 55-inch 4K Ultra HD OLED Smart Google TV",
            "category": "Home Appliances",
            "subcategory": "Smart Living",
            "brand": "Sony",
            "price": 114990.0,
            "discount": 15.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=700&auto=format&fit=crop&q=80"],
            "description": "Cognitive Processor XR delivers pure OLED infinite contrast with Acoustic Surface Audio+ where sound comes directly from the entire screen.",
            "specs": {"Display": "55-inch 4K OLED 120Hz", "Processor": "Cognitive Processor XR", "Audio": "Dolby Atmos Acoustic Surface Audio+", "OS": "Google TV with Hands-Free Mic"}
        },
        {
            "name": "Hurom H-200 Easy Clean Cold Press Slow Juicer",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Hurom",
            "price": 31990.0,
            "discount": 12.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=700&auto=format&fit=crop&q=80"],
            "description": "Self-feeding slow masticating cold press juicer (43 RPM) preserving 100% natural enzymes and vitamins with no-strainer 60-second cleanup.",
            "specs": {"RPM": "43 RPM Slow Squeezing", "Feed Chute": "Mega Hopper for Whole Apples", "Extraction": "Zero Strainer Mesh", "Warranty": "10 Years on Motor"}
        },
        {
            "name": "Instant Pot Duo Plus 9-in-1 Smart Multi-Cooker (6L)",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Instant Pot",
            "price": 9999.0,
            "discount": 25.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1544233726-9f1d2b27be8b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1544233726-9f1d2b27be8b?w=700&auto=format&fit=crop&q=80"],
            "description": "9-in-1 appliance: Pressure Cooker, Slow Cooker, Rice Cooker, Steamer, Sauté Pan, Yogurt Maker, Sous Vide, Sterilizer, and Food Warmer.",
            "specs": {"Capacity": "6 Liters (5.7L)", "Programs": "15 One-Touch Smart Programs", "Safety": "10+ Certified Safety Protections", "Inner Pot": "Food Grade 304 Stainless Steel"}
        },
        {
            "name": "KitchenAid Artisan 4.8L Tilt-Head Stand Mixer",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "KitchenAid",
            "price": 38990.0,
            "discount": 10.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=700&auto=format&fit=crop&q=80"],
            "description": "Iconic die-cast metal construction with planetary 59-point mixing action. Includes flat beater, dough hook, wire whip, and pouring shield.",
            "specs": {"Capacity": "4.8 Liters Stainless Steel Bowl", "Motor": "Direct Drive 300W High Torque", "Speeds": "10 Speed Control", "Warranty": "5 Years Guarantee"}
        },
        {
            "name": "Philips Garment Steamer 1800W with Multi-Angle Board",
            "category": "Home Appliances",
            "subcategory": "Laundry & Cleaning",
            "brand": "Philips",
            "price": 8490.0,
            "discount": 20.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1584990347449-399a9b70b5ee?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1584990347449-399a9b70b5ee?w=700&auto=format&fit=crop&q=80"],
            "description": "Continuous 35g/min powerful steam removes stubborn wrinkles from silks, sarees, suits, and daily wear without burning fabric.",
            "specs": {"Power": "1800 Watts", "Steam Output": "35 g/min", "Water Tank": "1.4 Liters Detachable", "Board": "Tilting Multi-Angle Ergonomic Board"}
        },
        {
            "name": "Dyson Purifier Hot+Cool HEPA Air Purifier & Heater",
            "category": "Home Appliances",
            "subcategory": "Cooling & Heating",
            "brand": "Dyson",
            "price": 54900.0,
            "discount": 5.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1550985543-f47f38aeee65?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1550985543-f47f38aeee65?w=700&auto=format&fit=crop&q=80"],
            "description": "Fully sealed HEPA H13 filtration captures 99.95% of pollutants and viruses. Fast heating in winter, cooling fan in summer, and smart app reports.",
            "specs": {"Filtration": "HEPA H13 + Activated Carbon", "Coverage": "Up to 400 sq. ft.", "Oscillation": "350 Degree Airflow", "Smart Control": "MyDyson App + Voice"}
        },
        {
            "name": "Prestige Tri-Ply Stainless Steel 4-Piece Cookware Set",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Prestige",
            "price": 4690.0,
            "discount": 30.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1584990347449-399a9b70b5ee?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1584990347449-399a9b70b5ee?w=700&auto=format&fit=crop&q=80"],
            "description": "Heavy-gauge 3-layer steel-aluminum-steel sandwich base ensures uniform heat distribution without burning food. Induction & gas compatible.",
            "specs": {"Material": "Tri-Ply Stainless Steel 304", "Includes": "Kadhai (26cm), Fry Pan (24cm), Saucepan (18cm), Glass Lids", "Warranty": "5 Years"}
        },
        {
            "name": "Pigeon 1.8L Stainless Steel Fast-Boiling Electric Kettle",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Pigeon",
            "price": 799.0,
            "discount": 40.0,
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1594213114663-ddf4f240f08d?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1594213114663-ddf4f240f08d?w=700&auto=format&fit=crop&q=80"],
            "description": "1500W fast boiling cordless kettle with 360-degree swivel power base, food-grade steel body, auto-cutoff, and boil dry protection.",
            "specs": {"Capacity": "1.8 Liters", "Power": "1500 Watts", "Safety": "Auto Cut-Off & Boil Dry", "Warranty": "1 Year Replacement"}
        },
        {
            "name": "Havells Induction Cooktop 2000W with Auto-Pan Sensor",
            "category": "Home Appliances",
            "subcategory": "Kitchen & Smart Home",
            "brand": "Havells",
            "price": 2999.0,
            "discount": 35.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=700&auto=format&fit=crop&q=80"],
            "description": "Microcrystalline ceramic glass induction plate with 8 Indian auto-cook menu options, touch sensor timer, and voltage surge protection.",
            "specs": {"Power": "2000 Watts", "Plate": "Ceramic Microcrystalline Glass", "Cooking Menus": "8 Preset Indian Menus", "Timer": "3 Hour Timer"}
        },

        # =========================================================================
        # --- 3. OTHER CATEGORIES ---
        # =========================================================================
        {
            "name": "Men's 2-Piece Slim Fit Tailored Formal Suit",
            "category": "Men's Fashion",
            "brand": "Raymond",
            "price": 9490.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=700&auto=format&fit=crop&q=80"],
            "description": "Sharp tailored 2-piece blazer and trouser suit in fine poly-wool blend. Perfect for boardroom meetings and formal receptions.",
            "specs": {"Material": "Poly-Wool Blend", "Fit": "Custom Slim Fit", "Color": "Charcoal Grey"}
        },
        {
            "name": "Men's Western Indigo Denim Shirt",
            "category": "Men's Fashion",
            "brand": "Levi's",
            "price": 1999.0,
            "discount": 20.0,
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=700&auto=format&fit=crop&q=80"],
            "description": "Timeless western denim shirt in indigo wash with dual flap chest pockets and pearlized snap buttons.",
            "specs": {"Material": "100% Cotton Denim", "Fit": "Slim Fit", "Collar": "Spread Collar"}
        },
        {
            "name": "Men's Classic Cotton Pique Polo T-Shirt",
            "category": "Men's Fashion",
            "brand": "Ralph Lauren",
            "price": 3290.0,
            "discount": 10.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=700&auto=format&fit=crop&q=80"],
            "description": "Breathable cotton pique polo featuring ribbed collar, embroidered chest logo, and durable side vents.",
            "specs": {"Material": "100% Breathable Pique Cotton", "Fit": "Custom Slim", "Color": "Navy Blue"}
        },
        {
            "name": "Nike Air Zoom Pegasus 40 Running Shoes",
            "category": "Footwear",
            "brand": "Nike",
            "price": 10495.0,
            "discount": 10.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700&auto=format&fit=crop&q=80"],
            "description": "Responsive road running shoe with dual Nike Air Zoom units and lightweight engineered mesh upper for endurance.",
            "specs": {"Upper": "Engineered Mesh", "Cushioning": "Nike React Foam + Zoom Air", "Surface": "Road Running"}
        },
        {
            "name": "Adidas Ultraboost Light Running Shoes",
            "category": "Footwear",
            "brand": "Adidas",
            "price": 14999.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=700&auto=format&fit=crop&q=80"],
            "description": "Lightest Boost midsole ever created, delivering unmatched energy return and Continental rubber outsole grip.",
            "specs": {"Midsole": "Light BOOST", "Upper": "PRIMEKNIT+ Textile", "Color": "Core Black / White"}
        },
        {
            "name": "Puma Smash v2 Classic Leather Sneakers",
            "category": "Footwear",
            "brand": "Puma",
            "price": 2999.0,
            "discount": 40.0,
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=700&auto=format&fit=crop&q=80"],
            "description": "Tennis-inspired lifestyle leather sneakers with SoftFoam+ sockliner for cloud-like cushioning throughout the day.",
            "specs": {"Upper": "Genuine Leather", "Insole": "SoftFoam+ Cushioning", "Color": "Puma White"}
        },
        {
            "name": "iPhone 15 Pro 128GB Titanium",
            "category": "Electronics",
            "brand": "Apple",
            "price": 129900.0,
            "discount": 5.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=700&auto=format&fit=crop&q=80"],
            "description": "Forged in aerospace-grade titanium with the breakthrough A17 Pro chip, 48MP camera system, and USB-C with USB 3 speeds.",
            "specs": {"Chip": "A17 Pro", "Display": "6.1-inch Super Retina XDR 120Hz", "Storage": "128GB"}
        },
        {
            "name": "MacBook Air 13.6-inch M3 Chip",
            "category": "Electronics",
            "brand": "Apple",
            "price": 114900.0,
            "discount": 0.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=700&auto=format&fit=crop&q=80"],
            "description": "Lean, mean M3 machine. Up to 18 hours of battery life, Liquid Retina display, and MagSafe 3 charging.",
            "specs": {"Processor": "Apple M3 8-Core CPU / 8-Core GPU", "RAM": "8GB Unified", "SSD": "256GB NVMe"}
        },
        {
            "name": "Sony WH-1000XM5 Noise Cancelling Headphones",
            "category": "Electronics",
            "brand": "Sony",
            "price": 29990.0,
            "discount": 10.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700&auto=format&fit=crop&q=80"],
            "description": "Industry-leading noise canceling with 8 microphones, Auto NC Optimizer, and 30-hour battery life.",
            "specs": {"Battery Life": "30 Hours with ANC", "Drivers": "30mm Precision Engineered", "Codecs": "LDAC, AAC, SBC"}
        },
        {
            "name": "Dior Sauvage Eau de Parfum 100ml",
            "category": "Beauty & Grooming",
            "brand": "Dior",
            "price": 11500.0,
            "discount": 0.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=700&auto=format&fit=crop&q=80"],
            "description": "Luxury fragrance with spicy Calabrian bergamot, smoky vanilla extract, and woody amber notes.",
            "specs": {"Volume": "100 ml", "Concentration": "Eau de Parfum (EDP)", "Longevity": "12+ Hours"}
        },
        {
            "name": "L'Oreal Paris Revitalift Hyaluronic Acid Serum",
            "category": "Beauty & Grooming",
            "brand": "L'Oreal",
            "price": 999.0,
            "discount": 15.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=700&auto=format&fit=crop&q=80"],
            "description": "1.5% pure hyaluronic acid face serum that deeply hydrates, plumps skin, and visibly reduces fine lines.",
            "specs": {"Volume": "30 ml", "Skin Type": "All Skin Types", "Paraben Free": "Yes"}
        },
        {
            "name": "Casio G-Shock Analog-Digital Solar Watch",
            "category": "Watches & Accessories",
            "brand": "Casio",
            "price": 8495.0,
            "discount": 10.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=700&auto=format&fit=crop&q=80"],
            "description": "Shock-resistant 200M water-resistant wristwatch with world time, 5 alarms, and solar battery power.",
            "specs": {"Water Resistance": "200 Meters", "Dial Glass": "Mineral Glass", "Shock Resistant": "Yes"}
        },
        {
            "name": "Ray-Ban Aviator Classic Polarized Sunglasses",
            "category": "Watches & Accessories",
            "brand": "Ray-Ban",
            "price": 7990.0,
            "discount": 15.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=700&auto=format&fit=crop&q=80"],
            "description": "Timeless teardrop pilot shape in gold metal frame with crystal green G-15 polarized lenses providing 100% UV protection.",
            "specs": {"Lens": "Polarized G-15 Crystal", "Frame": "Metal Gold Finish", "UV Protection": "100% UV400"}
        },
        {
            "name": "LEGO Star Wars Millennium Falcon Building Kit",
            "category": "Kids & Toys",
            "brand": "LEGO",
            "price": 14999.0,
            "discount": 5.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?w=700&auto=format&fit=crop&q=80"],
            "description": "Iconic Star Wars starship building toy featuring 1,351 pieces, opening cockpit, rotating turrets, and 7 minifigures.",
            "specs": {"Pieces": "1351", "Age Group": "9+ Years", "Minifigures": "7 Characters"}
        },
        {
            "name": "Yonex Astrox 99 Pro Badminton Racquet",
            "category": "Sports & Fitness",
            "brand": "Yonex",
            "price": 16990.0,
            "discount": 15.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=700&auto=format&fit=crop&q=80"],
            "description": "Head-heavy power racquet built with Namd graphite for steep smashes and rapid recovery.",
            "specs": {"Weight": "3U (88g)", "Flex": "Stiff", "Frame": "HM Graphite + NAMD"}
        },
        {
            "name": "Atomic Habits by James Clear",
            "category": "Books",
            "brand": "Penguin Random House",
            "price": 499.0,
            "discount": 30.0,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=700&auto=format&fit=crop&q=80",
            "images": ["https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=700&auto=format&fit=crop&q=80"],
            "description": "An easy & proven way to build good habits & break bad ones. Over 15 million copies sold worldwide.",
            "specs": {"Author": "James Clear", "Format": "Paperback", "Pages": "320"}
        }
    ]

    for p in products_data:
        cat_id = category_map.get(p["category"], list(category_map.values())[0])
        orig_price = p["price"] / (1 - (p["discount"]/100.0)) if p["discount"] > 0 else p["price"]
        
        prod = Product(
            name=p["name"],
            category_id=cat_id,
            subcategory=p.get("subcategory"),
            brand=p["brand"],
            description=p["description"],
            price=p["price"],
            original_price=round(orig_price, 2),
            discount=p["discount"],
            rating=p["rating"],
            review_count=random.randint(45, 820),
            image=p["image"],
            images=json.dumps(p.get("images", [p["image"]])),
            stock=random.randint(15, 120),
            specifications=json.dumps(p["specs"])
        )
        db.add(prod)

    db.commit()

    # Seeding Users
    print("Seeding Users...")
    user_data = [
        {"name": "Ananya Sen", "email": "ananya@example.com", "profile_image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ananya"},
        {"name": "Rahul Sharma", "email": "rahul@example.com", "profile_image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Rahul"},
        {"name": "Priya Patel", "email": "priya@example.com", "profile_image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya"},
        {"name": "Aditya Verma", "email": "aditya@example.com", "profile_image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Aditya"},
        {"name": "Sneha Reddy", "email": "sneha@example.com", "profile_image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sneha"}
    ]
    users = []
    for u in user_data:
        user = User(name=u["name"], email=u["email"], password_hash="hashed_password", profile_image=u["profile_image"])
        db.add(user)
        users.append(user)
    db.commit()

    # Seeding Reviews & Price Histories
    print("Seeding Category-Specific Reviews & Price Histories...")
    all_prods = db.query(Product).all()

    reviews_by_category = {
        "Women's Fashion": {
            "pos": ["The fabric is soft and feels very luxurious. Sizing and color are true to the images!", "Received so many compliments when I wore this! Sturdy stitching and great fit.", "Beautiful drape and very breathable material. Perfect for parties and everyday wear."],
            "neg": ["Length is a little long for my height, needed minor alteration.", "Color was slightly darker than the product photos, but still nice.", "Delivery was delayed by two days."]
        },
        "Home Appliances": {
            "pos": ["Completely revolutionized our daily routine! Whisper quiet, powerful, and very energy efficient.", "Premium build quality and modern aesthetic. Easy to operate with rich presets.", "Outstanding performance! Heats/cleans evenly and saves significant cooking & cleaning time."],
            "neg": ["Takes a little time to read through all smart settings in manual.", "App setup requires steady 2.4GHz Wi-Fi.", "Cord length could be slightly longer."]
        },
        "default": {
            "pos": ["Outstanding build quality and premium performance! Exceeded expectations.", "Works flawlessly right out of the box. Highly recommended!", "Very reliable and well worth the price."],
            "neg": ["User manual could have more detailed instructions.", "Price is on the higher side.", "Packaging could be more eco-friendly."]
        }
    }

    for prod in all_prods:
        cat_name = prod.category.name if prod.category else "default"
        review_pool = reviews_by_category.get(cat_name, reviews_by_category.get("default"))

        # 4 Reviews per product
        r1 = Review(product_id=prod.id, user_id=users[0].id, rating=5.0, review_text=review_pool["pos"][0], sentiment="Positive")
        r2 = Review(product_id=prod.id, user_id=users[1].id, rating=4.5, review_text=review_pool["pos"][1], sentiment="Positive")
        r3 = Review(product_id=prod.id, user_id=users[2].id, rating=4.0, review_text="Good overall product. Meets expectations with minor trade-offs.", sentiment="Neutral")
        r4 = Review(product_id=prod.id, user_id=users[3].id, rating=2.5, review_text=review_pool["neg"][0], sentiment="Negative")
        db.add_all([r1, r2, r3, r4])

        # 10 Price History records spanning last 30 days
        base = prod.price
        for i in range(10):
            variance = 1.0 + random.uniform(-0.12, 0.08)
            h_price = round(base * variance, 2)
            if i == 9:
                h_price = base
            
            days_ago = (9 - i) * 3
            db.add(PriceHistory(
                product_id=prod.id,
                price=h_price,
                source=random.choice(["Official Store", "Amazon", "Flipkart"]),
                recorded_at=datetime.now() - timedelta(days=days_ago)
            ))

    db.commit()
    db.close()
    print(f"Database seeded successfully with {len(all_prods)} products! All Women's Fashion items unified.")

if __name__ == "__main__":
    seed_database()
