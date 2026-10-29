import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs('assets/images', exist_ok=True)

def create_gradient(width, height, color1, color2, vertical=True):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            val = int(255 * (y / height if vertical else x / width))
            mask_data.append(val)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

# 1. Login Telemetry Chart Banner (Exactly as seen in Screenshot 2 & 3)
def gen_login_banner():
    w, h = 720, 240
    img = create_gradient(w, h, (11, 19, 38), (17, 24, 39), vertical=True)
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(24, 38, 68), width=1)
    for y in range(0, h, 30):
        draw.line([(0, y), (w, y)], fill=(24, 38, 68), width=1)
        
    # Top 4 metric boxes
    boxes = [
        ("ACTIVE ASSETS", "1,420", "+18.4% YoY"),
        ("AVERAGE YIELD", "9.2%", "Prime Commercial"),
        ("RERA COMPLIANCE", "100%", "Tier-1 Vetted"),
        ("ESCROW SPEED", "2.1 Min", "Instant Verify")
    ]
    box_w = 150
    for i, (title, val, sub) in enumerate(boxes):
        bx = 20 + i * 170
        by = 18
        draw.rounded_rectangle([(bx, by), (bx + box_w, by + 58)], radius=6, fill=(15, 23, 42), outline=(37, 99, 235))
        draw.text((bx + 10, by + 6), title, fill=(148, 163, 184))
        draw.text((bx + 10, by + 22), val, fill=(248, 250, 252))
        draw.text((bx + 10, by + 40), sub, fill=(52, 211, 153))

    # Line Chart with glowing nodes
    points = [
        (40, 180), (120, 170), (200, 140), (280, 160), 
        (360, 115), (440, 130), (520, 95), (600, 110), (680, 75)
    ]
    # Draw glow underneath
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(245, 158, 11), width=4)
    for pt in points:
        draw.ellipse([(pt[0]-4, pt[1]-4), (pt[0]+4, pt[1]+4)], fill=(255, 255, 255), outline=(245, 158, 11), width=2)
        
    # Bottom badge
    draw.rounded_rectangle([(30, h - 38), (520, h - 10)], radius=4, fill=(0, 0, 0), outline=(245, 158, 11))
    draw.text((40, h - 30), ">> Live Real Estate Portfolio & Yield Telemetry Engine", fill=(255, 255, 255))
    
    path = 'assets/images/login-chart-banner.webp'
    img.save(path, 'WEBP', quality=85)
    print(f"Saved {path}: {os.path.getsize(path)/1024:.1f} KB")

# 2. Hero Estate Banner
def gen_hero_banner():
    w, h = 1200, 600
    img = create_gradient(w, h, (18, 9, 36), (42, 18, 76), vertical=True)
    draw = ImageDraw.Draw(img)
    
    # Draw architectural skyline silhouettes & warm ambient windows
    # Background towers
    towers = [
        (100, 220, 90, 380, (26, 16, 52)),
        (220, 160, 110, 440, (32, 19, 64)),
        (360, 100, 140, 500, (40, 24, 78)),
        (530, 140, 120, 460, (30, 18, 60)),
        (680, 80, 160, 520, (45, 28, 86)),
        (870, 150, 130, 450, (35, 20, 68)),
        (1030, 200, 110, 400, (28, 16, 55))
    ]
    for x, y, tw, th, col in towers:
        draw.rectangle([(x, y), (x + tw, y + th)], fill=col)
        # Windows
        for wx in range(x + 10, x + tw - 10, 20):
            for wy in range(y + 20, y + th - 20, 28):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([(wx, wy), (wx + 10, wy + 16)], fill=(251, 191, 36, 180))
                elif (wx + wy) % 5 == 0:
                    draw.rectangle([(wx, wy), (wx + 10, wy + 16)], fill=(147, 197, 253, 140))
                    
    # Foreground glowing glass villa structure
    draw.polygon([(250, 550), (450, 400), (850, 400), (1050, 550)], fill=(24, 12, 48))
    draw.rectangle([(380, 380), (820, 550)], fill=(35, 18, 68), outline=(245, 158, 11), width=2)
    # Warm pool glow
    draw.rounded_rectangle([(300, 520), (900, 590)], radius=15, fill=(14, 165, 233))
    
    # Overlay gradient at bottom for text contrast
    for y in range(450, 600):
        alpha = int(255 * ((y - 450) / 150))
        draw.line([(0, y), (w, y)], fill=(15, 6, 30))
        
    path = 'assets/images/hero-estate-banner.webp'
    img.save(path, 'WEBP', quality=82)
    print(f"Saved {path}: {os.path.getsize(path)/1024:.1f} KB")

# 3. Project Cards (Villa, HighRise, Commercial, Township, Penthouse)
def gen_project_img(name, title_text, cat_text, price_text, base_cols):
    w, h = 640, 420
    c1, c2, accent = base_cols
    img = create_gradient(w, h, c1, c2, vertical=True)
    draw = ImageDraw.Draw(img)
    
    # Modern architectural drawing geometry
    # Grid & perspective
    for i in range(0, w, 35):
        draw.line([(i, 0), (i, h)], fill=(c1[0]+15, c1[1]+15, c1[2]+20), width=1)
    
    # Modern luxury structure
    draw.polygon([(80, 360), (160, 160), (480, 130), (560, 360)], fill=(c2[0]+15, c2[1]+15, c2[2]+20))
    # Glass balconies / windows
    for floor in range(160, 340, 32):
        draw.rectangle([(160, floor), (480, floor + 20)], fill=(15, 23, 42), outline=accent, width=1)
        for glass in range(180, 460, 45):
            draw.rectangle([(glass, floor + 4), (glass + 28, floor + 16)], fill=(224, 242, 254))
            
    # Pool / Green garden
    draw.rectangle([(0, 360), (w, h)], fill=(16, 185, 129) if "Green" in cat_text or "Villa" in cat_text else (14, 116, 144))
    
    # Top tags
    draw.rounded_rectangle([(24, 20), (160, 52)], radius=16, fill=(15, 23, 42), outline=accent, width=1)
    draw.text((38, 28), "[RERA VERIFIED]", fill=(245, 158, 11))
    
    draw.rounded_rectangle([(w - 180, 20), (w - 24, 52)], radius=16, fill=accent)
    draw.text((w - 165, 28), cat_text, fill=(255, 255, 255))
    
    # Bottom glass banner
    draw.rounded_rectangle([(24, h - 85), (w - 24, h - 20)], radius=12, fill=(15, 23, 42))
    draw.text((45, h - 75), title_text, fill=(255, 255, 255))
    draw.text((45, h - 48), price_text, fill=(245, 158, 11))
    draw.text((w - 180, h - 60), "ROI: 14.8% p.a. >>", fill=(52, 211, 153))
    
    path = f'assets/images/{name}.webp'
    img.save(path, 'WEBP', quality=80)
    print(f"Saved {path}: {os.path.getsize(path)/1024:.1f} KB")

# 4. Advisor portraits
def gen_advisor_img(name, initials, role, exp):
    w, h = 360, 360
    # Clean corporate gradient
    img = create_gradient(w, h, (30, 27, 75), (67, 56, 202), vertical=True)
    draw = ImageDraw.Draw(img)
    
    # Avatar Circle
    cx, cy = w // 2, 130
    draw.ellipse([(cx - 70, cy - 70), (cx + 70, cy + 70)], fill=(245, 158, 11))
    draw.ellipse([(cx - 65, cy - 65), (cx + 65, cy + 65)], fill=(30, 27, 75))
    draw.text((cx - 24, cy - 18), initials, fill=(255, 255, 255))
    
    # Star badge
    draw.rounded_rectangle([(cx - 60, cy + 85), (cx + 60, cy + 115)], radius=12, fill=(245, 158, 11))
    draw.text((cx - 45, cy + 92), "Top Advisor", fill=(15, 23, 42))
    
    # Details card
    draw.text((cx - 80, 260), role, fill=(255, 255, 255))
    draw.text((cx - 60, 290), exp, fill=(199, 210, 254))
    
    path = f'assets/images/{name}.webp'
    img.save(path, 'WEBP', quality=85)
    print(f"Saved {path}: {os.path.getsize(path)/1024:.1f} KB")

# 5. Market Report / Infographic WebP
def gen_market_infographic():
    w, h = 600, 380
    img = create_gradient(w, h, (15, 23, 42), (30, 41, 59), vertical=True)
    draw = ImageDraw.Draw(img)
    
    draw.text((30, 25), "STACKLY 2026 HOUSING MARKET INDEX", fill=(245, 158, 11))
    draw.text((30, 50), "Salem, Chennai & Bengaluru Appreciation Benchmarks", fill=(148, 163, 184))
    
    # Bar Chart
    bars = [
        ("Salem IT Corridor", 185, (245, 158, 11)),
        ("Fairlands Luxury", 140, (14, 165, 233)),
        ("Yercaud Estates", 120, (16, 185, 129)),
        ("Bengaluru North", 210, (168, 85, 247)),
        ("OMR Tech Belt", 165, (236, 72, 153))
    ]
    for i, (label, val, col) in enumerate(bars):
        y = 100 + i * 50
        draw.text((30, y + 6), label, fill=(255, 255, 255))
        draw.rounded_rectangle([(200, y), (200 + val * 1.6, y + 26)], radius=6, fill=col)
        draw.text((210 + int(val * 1.6), y + 6), f"+{val//10}.{val%10}%", fill=(255, 255, 255))
        
    path = 'assets/images/market-chart-2026.webp'
    img.save(path, 'WEBP', quality=85)
    print(f"Saved {path}: {os.path.getsize(path)/1024:.1f} KB")

# Generate all
gen_login_banner()
gen_hero_banner()
gen_project_img("project-luxury-villa", "The Grand Imperial Villas", "Ultra Luxury 4-5 BHK", "INR 1.85 Cr - 4.50 Cr", ((20, 15, 45), (45, 30, 85), (245, 158, 11)))
gen_project_img("project-skyline-tower", "Stackly Pinnacle Sky-Suites", "Modern High-Rise", "INR 72 Lakh - 1.45 Cr", ((15, 25, 55), (30, 50, 100), (59, 130, 246)))
gen_project_img("project-commercial-park", "CyberEdge Business Square", "Grade-A Commercial SCO", "INR 1.10 Cr - 6.80 Cr", ((25, 15, 35), (60, 25, 60), (236, 72, 153)))
gen_project_img("project-eco-township", "GreenMeadows Integrated City", "Plotted & Villa Township", "INR 38 Lakh - 85 Lakh", ((15, 35, 25), (25, 70, 45), (16, 185, 129)))
gen_project_img("project-penthouse", "The Solitaire Sky Penthouse", "360 Panoramic Deck", "INR 3.20 Cr - 5.90 Cr", ((35, 20, 40), (75, 35, 65), (245, 158, 11)))
gen_advisor_img("advisor-shilpi", "SS", "Dr. / Adv. Shilpi Singh", "16+ Yrs Commercial M&A")
gen_advisor_img("advisor-ananya", "AS", "Ananya Sen, RICS", "12+ Yrs High-Yield Advisory")
gen_advisor_img("advisor-meera", "MN", "Meera Nair, High Court", "18+ Yrs RERA Due Diligence")
gen_advisor_img("advisor-priya", "PS", "Priya Sharma, CFA", "10+ Yrs NRI Cross-Border")
gen_market_infographic()
print("All images generated successfully!")
