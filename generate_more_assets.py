import os
from PIL import Image, ImageDraw

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

# Blog covers
blogs = [
    ("blog-rera-guide", "RERA 2.0 Compliance & Title Due Diligence", "Legal Advisory", (20, 10, 40), (45, 20, 75)),
    ("blog-tax-reit", "Capital Gains 54F & Commercial REIT Yields", "Wealth & Tax", (10, 25, 45), (25, 55, 95)),
    ("blog-proptech-ai", "AI Property Valuation: The Future of PropTech", "Technology", (15, 35, 30), (30, 75, 60)),
    ("blog-nri-investment", "Complete NRI Real Estate Guide India 2026", "Global Investors", (35, 20, 20), (80, 40, 35)),
    ("blog-emerging-corridors", "Salem-Coimbatore-Bengaluru Express Corridors", "Market Insights", (30, 25, 10), (70, 55, 20)),
    ("blog-luxury-villas", "Smart Sustainable Architecture in Modern Estates", "Architecture", (25, 15, 45), (55, 35, 95))
]

for name, title, tag, c1, c2 in blogs:
    w, h = 600, 360
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    # Abstract geometric blueprint lines
    for i in range(0, w, 40):
        draw.line([(i, 0), (i, h)], fill=(c1[0]+20, c1[1]+20, c1[2]+25), width=1)
    for j in range(0, h, 40):
        draw.line([(0, j), (w, j)], fill=(c1[0]+20, c1[1]+20, c1[2]+25), width=1)
    
    # Glowing tag badge
    draw.rounded_rectangle([(30, 30), (220, 65)], radius=12, fill=(245, 158, 11))
    draw.text((45, 40), tag.upper(), fill=(15, 23, 42))
    
    # Title overlay card
    draw.rounded_rectangle([(30, h - 110), (w - 30, h - 30)], radius=12, fill=(15, 23, 42))
    draw.text((50, h - 95), title[:38], fill=(255, 255, 255))
    draw.text((50, h - 65), "Read Strategic Intelligence Report >>", fill=(245, 158, 11))
    
    path = f'assets/images/{name}.webp'
    img.save(path, 'WEBP', quality=80)
    print(f"Saved {path}: {os.path.getsize(path)/1024:.1f} KB")

# Service Cards
services = [
    ("service-residential", "Residential Acquisition & Ultra Luxury Estates", (30, 15, 50), (60, 25, 90)),
    ("service-commercial", "Pre-Leased Commercial & Grade-A IT Parks", (15, 30, 50), (30, 65, 100)),
    ("service-nri", "NRI Cross-Border Investment & Repatriation Desk", (20, 40, 30), (40, 80, 60)),
    ("service-legal", "120-Point Title Search, RERA & Legal Audit", (40, 20, 20), (90, 45, 35)),
    ("service-homeloan", "Structured Mortgage & Lowest Bank Rate Advisory", (35, 30, 15), (80, 65, 30)),
    ("service-portfolio", "Private Portfolio Management & 1031/54F Exits", (25, 15, 40), (60, 35, 80))
]

for name, title, c1, c2 in services:
    w, h = 540, 320
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    # Isometric cube / architectural structure
    draw.polygon([(180, 160), (270, 110), (360, 160), (270, 210)], fill=(c2[0]+30, c2[1]+30, c2[2]+30))
    draw.polygon([(180, 160), (270, 210), (270, 290), (180, 240)], fill=(c2[0]+15, c2[1]+15, c2[2]+15))
    draw.polygon([(270, 210), (360, 160), (360, 240), (270, 290)], fill=(c2[0]+45, c2[1]+45, c2[2]+45))
    
    draw.rounded_rectangle([(25, h - 80), (w - 25, h - 20)], radius=10, fill=(15, 23, 42))
    draw.text((45, h - 65), title[:36], fill=(255, 255, 255))
    draw.text((45, h - 42), "Verified Advisory Track Record: 100% >>", fill=(245, 158, 11))
    
    path = f'assets/images/{name}.webp'
    img.save(path, 'WEBP', quality=80)
    print(f"Saved {path}: {os.path.getsize(path)/1024:.1f} KB")

print("Additional WebP assets generated successfully!")
