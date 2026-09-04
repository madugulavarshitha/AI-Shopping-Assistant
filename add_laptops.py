import json
import random
from datetime import datetime, timedelta
from database.connection import SessionLocal
from models.product import Product
from models.category import Category
from models.review import Review
from models.price_history import PriceHistory
from models.user import User

def add_laptops_and_gadgets():
    db = SessionLocal()
    
    # Ensure Electronics category exists
    cat = db.query(Category).filter(Category.name.ilike("%Electronics%")).first()
    if not cat:
        cat = Category(name="Electronics")
        db.add(cat)
        db.commit()
        db.refresh(cat)
    
    users = db.query(User).all()
    if not users:
        print("No users found to attach reviews.")
        users = []

    laptops_data = [
        {
            "name": "HP 15s Ryzen 5 Hexa-Core 16GB RAM 512GB SSD Laptop",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "HP",
            "price": 44990.0,
            "discount": 18.0,
            "rating": 4.5,
            "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=700&auto=format&fit=crop&q=80",
            "description": "HP 15s equipped with AMD Ryzen 5 5500U processor, 16GB DDR4 RAM, 512GB NVMe SSD, 15.6-inch FHD Anti-Glare micro-edge display, and fast charging.",
            "specs": {"Processor": "AMD Ryzen 5 5500U", "RAM": "16 GB DDR4", "Storage": "512 GB NVMe SSD", "Display": "15.6\" FHD 1920x1080", "OS": "Windows 11 Home", "Weight": "1.69 kg"}
        },
        {
            "name": "Lenovo IdeaPad Slim 3 12th Gen Intel Core i3 Thin & Light Laptop",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "Lenovo",
            "price": 36990.0,
            "discount": 25.0,
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=700&auto=format&fit=crop&q=80",
            "description": "Lenovo IdeaPad Slim 3 featuring 12th Gen Intel Core i3-1215U, 8GB RAM, 512GB SSD, Dolby Audio speakers, privacy camera shutter, and military-grade durability.",
            "specs": {"Processor": "Intel Core i3-1215U (12th Gen)", "RAM": "8 GB DDR4", "Storage": "512 GB SSD", "Display": "15.6\" FHD IPS", "OS": "Windows 11", "Battery": "Up to 7 Hours"}
        },
        {
            "name": "ASUS Vivobook 15 Intel Core i5 12th Gen 16GB RAM Laptop",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "ASUS",
            "price": 49990.0,
            "discount": 22.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=700&auto=format&fit=crop&q=80",
            "description": "Sleek ASUS Vivobook 15 with Intel Core i5-1235U, 16GB RAM, 512GB PCIe 4.0 SSD, fingerprint sensor, 180-degree lay-flat hinge, and antibacterial guard.",
            "specs": {"Processor": "Intel Core i5-1235U", "RAM": "16 GB DDR4", "Storage": "512 GB PCIe 4.0 SSD", "Display": "15.6\" FHD NanoEdge", "Weight": "1.7 kg"}
        },
        {
            "name": "Dell 15 Thin & Light Laptop Intel Core i3 8GB 512GB SSD",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "Dell",
            "price": 37990.0,
            "discount": 15.0,
            "rating": 4.3,
            "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=700&auto=format&fit=crop&q=80",
            "description": "Dell 15 laptop with 12th Gen Intel Core i3-1215U, spill-resistant keyboard, Dell ComfortView low blue light software, and rapid express charging.",
            "specs": {"Processor": "Intel Core i3-1215U", "RAM": "8 GB RAM", "Storage": "512 GB SSD", "Display": "15.6\" FHD 120Hz", "Warranty": "1 Year Onsite"}
        },
        {
            "name": "Acer Aspire Lite AMD Ryzen 5 Hexa-Core 16GB RAM Laptop",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "Acer",
            "price": 41990.0,
            "discount": 28.0,
            "rating": 4.4,
            "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=700&auto=format&fit=crop&q=80",
            "description": "Premium metal-body Acer Aspire Lite with AMD Ryzen 5 5500U, 16GB dual-channel RAM, ultra-fast 512GB SSD, and Type-C multi-display connectivity.",
            "specs": {"Processor": "AMD Ryzen 5 5500U", "RAM": "16 GB DDR4", "Storage": "512 GB SSD", "Body": "Aluminum Metal Finish", "Weight": "1.59 kg"}
        },
        {
            "name": "ASUS TUF Gaming F15 Intel Core i5 RTX 3050 Gaming Laptop",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "ASUS",
            "price": 54990.0,
            "discount": 20.0,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1542393545-10f5cde2c810?w=700&auto=format&fit=crop&q=80",
            "description": "High-performance gaming laptop with Intel Core i5-11400H, NVIDIA GeForce RTX 3050 4GB GPU, 144Hz FHD gaming display, and RGB backlit keyboard.",
            "specs": {"Processor": "Intel Core i5-11400H", "GPU": "NVIDIA GeForce RTX 3050 4GB", "RAM": "16 GB DDR4", "Storage": "512 GB SSD", "Display": "15.6\" 144Hz FHD"}
        },
        {
            "name": "Lenovo ThinkPad E14 AMD Ryzen 7 16GB 512GB Business Laptop",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "Lenovo",
            "price": 64990.0,
            "discount": 12.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=700&auto=format&fit=crop&q=80",
            "description": "Legendary ThinkPad ergonomics with AMD Ryzen 7 7730U 8-Core processor, TrackPoint, TPM 2.0 security, aluminum chassis, and backlit keyboard.",
            "specs": {"Processor": "AMD Ryzen 7 7730U (8-Core)", "RAM": "16 GB DDR4", "Storage": "512 GB SSD", "Display": "14\" WUXGA 300 nits", "Security": "Fingerprint & TPM 2.0"}
        },
        {
            "name": "HP Pavilion Plus OLED Intel Core i7 13th Gen Ultrabook",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "HP",
            "price": 74990.0,
            "discount": 10.0,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=700&auto=format&fit=crop&q=80",
            "description": "Ultra-vibrant 2.8K 120Hz OLED display powered by 13th Gen Intel Core i7-13700H, 16GB LPDDR5x RAM, 1TB NVMe Gen4 SSD, and B&O tuned sound.",
            "specs": {"Processor": "Intel Core i7-13700H", "Display": "14\" 2.8K 120Hz OLED", "RAM": "16 GB LPDDR5x", "Storage": "1 TB NVMe SSD", "Weight": "1.44 kg"}
        },
        {
            "name": "Samsung Galaxy Book4 Intel Core i5 16GB 512GB Thin & Light Laptop",
            "category_id": cat.id,
            "subcategory": "Laptops",
            "brand": "Samsung",
            "price": 59990.0,
            "discount": 14.0,
            "rating": 4.6,
            "image": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=700&auto=format&fit=crop&q=80",
            "description": "Seamless Galaxy ecosystem connectivity, Intel Core i5 13th Gen, 15.6\" FHD anti-glare screen, ultra-slim 1.55kg metal body, and Dolby Atmos audio.",
            "specs": {"Processor": "Intel Core i5-1335U", "RAM": "16 GB LPDDR4x", "Storage": "512 GB NVMe SSD", "Battery": "Up to 12 Hours", "Weight": "1.55 kg"}
        }
    ]

    for p in laptops_data:
        # Check if product already exists
        existing = db.query(Product).filter(Product.name == p["name"]).first()
        if existing:
            continue
        
        orig_price = p["price"] / (1 - (p["discount"]/100.0)) if p["discount"] > 0 else p["price"]
        prod = Product(
            name=p["name"],
            category_id=p["category_id"],
            subcategory=p["subcategory"],
            brand=p["brand"],
            description=p["description"],
            price=p["price"],
            original_price=round(orig_price, 2),
            discount=p["discount"],
            rating=p["rating"],
            review_count=random.randint(50, 480),
            image=p["image"],
            images=json.dumps([p["image"]]),
            stock=random.randint(15, 60),
            specifications=json.dumps(p["specs"])
        )
        db.add(prod)
        db.commit()
        db.refresh(prod)

        # Add price history
        base = prod.price
        for i in range(10):
            variance = 1.0 + random.uniform(-0.08, 0.06)
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
        
        # Add reviews if users exist
        if users:
            reviews_text = [
                ("Excellent laptop performance! Fast boot times, great display and battery easily lasts 7+ hours.", 5.0, "Positive"),
                ("Superb value for money. Handles multitasking, coding and office work without any lag.", 4.5, "Positive"),
                ("Good build quality and tactile keyboard. Perfect for students and professionals.", 4.0, "Neutral")
            ]
            for u_idx, (r_txt, r_rat, r_sent) in enumerate(reviews_text):
                user_obj = users[u_idx % len(users)]
                db.add(Review(
                    product_id=prod.id,
                    user_id=user_obj.id,
                    rating=r_rat,
                    review_text=r_txt,
                    sentiment=r_sent
                ))

        db.commit()

    db.close()
    print("Laptops added successfully!")

if __name__ == "__main__":
    add_laptops_and_gadgets()
