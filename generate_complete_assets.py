import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs('assets/images', exist_ok=True)

try:
    font_lg = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 20)
    font_md = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 15)
    font_sm = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
    font_tag = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 12)
except:
    font_lg = font_md = font_sm = font_tag = ImageFont.load_default()

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

def draw_grid(draw, w, h, step=40, col=(255, 255, 255, 25)):
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=col, width=1)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=col, width=1)

def draw_modern_tower(draw, x, y, tw, th, base_col, win_col, roof_antenna=True):
    draw.rectangle([(x, y), (x + tw, y + th)], fill=base_col)
    cols = max(3, tw // 18)
    rows = max(5, th // 22)
    for c in range(cols):
        wx = x + 6 + c * (tw - 12) // cols
        for r in range(rows):
            wy = y + 10 + r * (th - 20) // rows
            if (c + r) % 3 != 0:
                draw.rectangle([(wx, wy), (wx + 10, wy + 14)], fill=win_col)
    if roof_antenna:
        mid = x + tw // 2
        draw.line([(mid, y), (mid, y - 30)], fill=(245, 158, 11), width=2)
        draw.ellipse([(mid - 3, y - 33), (mid + 3, y - 27)], fill=(239, 68, 68))

def draw_luxury_villa(draw, x, y, w, h, col1, col2):
    draw.polygon([(x + 40, y + 80), (x + w - 40, y + 80), (x + w - 70, y + h), (x + 70, y + h)], fill=col1)
    draw.rectangle([(x + 20, y + 20), (x + w - 100, y + 90)], fill=col2, outline=(245, 158, 11), width=2)
    draw.rectangle([(x + 35, y + 35), (x + w - 115, y + 75)], fill=(254, 240, 138))
    draw.rounded_rectangle([(x + 90, y + 100), (x + w - 30, y + 140)], radius=12, fill=(14, 165, 233))
    for px in range(x + 110, x + w - 50, 30):
        draw.line([(px, y + 120), (px + 18, y + 120)], fill=(255, 255, 255), width=2)

def save_webp(img, filename, max_kb=95):
    path = os.path.join('assets/images', filename)
    quality = 85
    img.save(path, 'WEBP', quality=quality)
    size_kb = os.path.getsize(path) / 1024
    while size_kb > max_kb and quality > 30:
        quality -= 5
        img.save(path, 'WEBP', quality=quality)
        size_kb = os.path.getsize(path) / 1024
    print(f"[{'OK' if size_kb <= 100 else 'FAIL'}] Saved {filename}: {size_kb:.1f} KB (quality={quality})")
    assert size_kb <= 100, f"File {filename} exceeded 100KB: {size_kb}KB"

# ==========================================================
# 1. HERO SLIDES (Animates across hero section)
# ==========================================================
hero_slides = [
    ("hero-slide-1.webp", "The Grand Aurora Towers", "Ultra-Luxury High-Rise in Fairlands Prime", (15, 7, 34), (45, 18, 78), "SKYLINE"),
    ("hero-slide-2.webp", "Fairlands Hillview Villa Sanctuary", "Private Heated Pools & 100% RERA Title", (10, 24, 40), (22, 60, 90), "VILLAS"),
    ("hero-slide-3.webp", "Zenith Commercial & IT Tech Park", "Pre-Leased to MNCs | 9.4% Rental Yield", (28, 16, 24), (70, 32, 54), "COMMERCIAL"),
    ("hero-slide-4.webp", "Verdant Eco Township & Plotted Habitat", "Solar Boulevards & Gated Clubhouse Living", (10, 35, 25), (25, 75, 55), "ECO-TOWNSHIP"),
    ("hero-slide-5.webp", "The Sky Penthouse Collection", "Duplex Terraces with Panoramic City Vistas", (24, 20, 10), (65, 50, 25), "PENTHOUSE")
]

for filename, title, sub, c1, c2, tag in hero_slides:
    w, h = 1000, 560
    img = create_gradient(w, h, c1, c2, vertical=True)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=50, col=(255, 255, 255, 18))
    
    towers = [
        (80, 200, 110, 360, (20, 12, 42), (251, 191, 36)),
        (210, 140, 130, 420, (28, 16, 56), (147, 197, 253)),
        (360, 90, 160, 470, (38, 22, 75), (253, 224, 71)),
        (540, 150, 140, 410, (30, 18, 62), (147, 197, 253)),
        (700, 110, 130, 450, (35, 20, 70), (251, 191, 36)),
        (850, 180, 110, 380, (25, 14, 50), (253, 224, 71))
    ]
    for x, y, tw, th, bcol, wcol in towers:
        draw_modern_tower(draw, x, y, tw, th, bcol, wcol)
        
    draw.polygon([(0, h), (300, 420), (700, 420), (w, h)], fill=(12, 6, 26))
    draw_luxury_villa(draw, 240, 380, 520, 160, (22, 12, 45), (42, 22, 85))
    
    draw.rounded_rectangle([(40, 40), (230, 78)], radius=18, fill=(245, 158, 11))
    draw.text((55, 52), f"FEATURED: {tag}", fill=(15, 23, 42), font=font_tag)
    
    draw.rounded_rectangle([(40, h - 110), (w - 40, h - 30)], radius=16, fill=(15, 7, 34))
    draw.line([(40, h - 110), (w - 40, h - 110)], fill=(245, 158, 11), width=2)
    draw.text((60, h - 96), title, fill=(255, 255, 255), font=font_lg)
    draw.text((60, h - 64), f">> {sub} | Verified 100% RERA Clearance", fill=(245, 158, 11), font=font_sm)
    
    save_webp(img, filename)

# ==========================================================
# 2. CATEGORY HUBS
# ==========================================================
cat_items = [
    ("cat-villas.webp", "Ultra Luxury Gated Villas", "4-5 BHK | Private Pool & Garden", (25, 12, 45), (65, 25, 95)),
    ("cat-apartments.webp", "High-Rise Sky Residences", "2, 3 & 4 BHK | Panoramic Views", (12, 28, 55), (28, 70, 120)),
    ("cat-commercial.webp", "Pre-Leased Commercial & SCO", "MNC Tenants | 9.2% Net Yield", (35, 20, 20), (90, 45, 40)),
    ("cat-plots.webp", "DTCP & RERA Approved Plots", "Clear Patta | 100% Due Diligence", (12, 38, 28), (28, 90, 65)),
    ("cat-farmhouses.webp", "Yercaud Foothills Farmhouses", "1-5 Acre Estates | Coffee Groves", (32, 25, 12), (80, 65, 25)),
    ("cat-penthouses.webp", "Crown Penthouses & Duplexes", "Private Elevators & Sky Decks", (40, 15, 45), (95, 35, 105))
]

for filename, title, sub, c1, c2 in cat_items:
    w, h = 500, 320
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=30, col=(255, 255, 255, 20))
    
    draw.polygon([(150, 140), (250, 90), (350, 140), (250, 190)], fill=(min(255, c2[0]+30), min(255, c2[1]+30), min(255, c2[2]+30)))
    draw.polygon([(150, 140), (250, 190), (250, 260), (150, 210)], fill=(min(255, c2[0]+10), min(255, c2[1]+10), min(255, c2[2]+10)))
    draw.polygon([(250, 190), (350, 140), (350, 210), (250, 260)], fill=(min(255, c2[0]+50), min(255, c2[1]+50), min(255, c2[2]+50)))
    
    draw.rectangle([(170, 160), (195, 185)], fill=(251, 191, 36))
    draw.rectangle([(290, 160), (315, 185)], fill=(147, 197, 253))
    
    draw.rounded_rectangle([(20, h - 80), (w - 20, h - 20)], radius=10, fill=(15, 23, 42))
    draw.text((36, h - 68), title, fill=(255, 255, 255), font=font_md)
    draw.text((36, h - 42), sub, fill=(245, 158, 11), font=font_sm)
    
    save_webp(img, filename)

# ==========================================================
# 3. LOCALITY SPOTLIGHTS
# ==========================================================
localities = [
    ("loc-fairlands.webp", "Fairlands Prime, Salem", "+24.8% Capital Growth", (28, 12, 50), (70, 28, 110)),
    ("loc-alagapuram.webp", "Alagapuram Green Boulevard", "+19.2% YoY Appreciation", (15, 30, 48), (35, 75, 115)),
    ("loc-yercaud.webp", "Yercaud Scenic Foothills", "+28.4% Holiday Rental Yield", (18, 38, 24), (40, 90, 60)),
    ("loc-hasthampatti.webp", "Hasthampatti Commercial Mile", "+21.5% Commercial Demand", (38, 24, 15), (95, 60, 30)),
    ("loc-suramangalam.webp", "Suramangalam Transit Junction", "+18.1% Infrastructure Boost", (20, 20, 45), (50, 50, 105)),
    ("loc-omr-chennai.webp", "OMR Expressway Chennai", "+22.6% IT Rental Demand", (30, 15, 40), (80, 35, 95))
]

for filename, title, sub, c1, c2 in localities:
    w, h = 500, 320
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=35, col=(255, 255, 255, 22))
    
    for bx in range(30, w - 40, 70):
        bh = 100 + (bx * 3) % 110
        draw.rectangle([(bx, h - 90 - bh), (bx + 55, h - 90)], fill=(min(255, c2[0]+15), min(255, c2[1]+15), min(255, c2[2]+15)))
        for wy in range(h - 85 - bh, h - 95, 20):
            draw.rectangle([(bx + 8, wy), (bx + 20, wy + 10)], fill=(253, 224, 71))
            draw.rectangle([(bx + 30, wy), (bx + 42, wy + 10)], fill=(147, 197, 253))
            
    draw.rounded_rectangle([(20, h - 75), (w - 20, h - 18)], radius=10, fill=(15, 23, 42))
    draw.text((35, h - 64), title, fill=(255, 255, 255), font=font_md)
    draw.text((35, h - 40), f"[GROWTH] {sub} | High Liquidity", fill=(52, 211, 153), font=font_sm)
    
    save_webp(img, filename)

# ==========================================================
# 4. FEATURED PROJECTS
# ==========================================================
featured_projects = [
    ("proj-aurora-residences.webp", "The Grand Aurora Residences", "Salem Fairlands | Rs 1.85 Cr - 3.40 Cr", (20, 10, 42), (55, 22, 95)),
    ("proj-zenith-tower.webp", "Zenith Commercial IT Hub", "CyberEdge Corridors | Rs 4.20 Cr+", (14, 25, 48), (32, 65, 110)),
    ("proj-solaris-estates.webp", "Solaris Hillview Luxury Villas", "Yercaud Foothills | Rs 2.10 Cr - 4.50 Cr", (25, 35, 20), (60, 85, 45)),
    ("proj-elysium-penthouse.webp", "The Elysium Penthouse Suites", "Alagapuram Heights | Rs 3.90 Cr+", (35, 18, 38), (85, 40, 85)),
    ("proj-verdant-gardens.webp", "Verdant Eco Township", "Salem Bypass Expressway | Rs 65 Lakhs+", (18, 32, 28), (42, 80, 65)),
    ("proj-signature-arcade.webp", "Signature Retail & Business Arcade", "Hasthampatti Main | Rs 1.25 Cr - 3.80 Cr", (38, 26, 12), (90, 65, 28))
]

for filename, title, sub, c1, c2 in featured_projects:
    w, h = 540, 340
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=36, col=(255, 255, 255, 18))
    
    draw.rounded_rectangle([(60, 60), (w - 60, 240)], radius=14, fill=(c1[0]+15, c1[1]+15, c1[2]+20), outline=(245, 158, 11), width=2)
    for gy in range(85, 220, 45):
        draw.rectangle([(80, gy), (w - 80, gy + 32)], fill=(14, 165, 233))
        draw.line([(80, gy + 16), (w - 80, gy + 16)], fill=(255, 255, 255), width=1)
        
    draw.rounded_rectangle([(30, 25), (220, 56)], radius=12, fill=(16, 185, 129))
    draw.text((45, 33), "100% RERA APPROVED", fill=(255, 255, 255), font=font_tag)
    
    draw.rounded_rectangle([(20, h - 85), (w - 20, h - 18)], radius=12, fill=(15, 23, 42))
    draw.text((36, h - 72), title, fill=(255, 255, 255), font=font_md)
    draw.text((36, h - 45), f"LOCATION: {sub}", fill=(245, 158, 11), font=font_sm)
    
    save_webp(img, filename)

# ==========================================================
# 5. CALCULATORS & FINANCIAL PROMISES
# ==========================================================
calcs = [
    ("calc-roi-visual.webp", "AI PropTech Yield Telemetry", "10-Year Capital Gain Simulation Engine", (15, 20, 42), (32, 50, 95)),
    ("calc-mortgage-visual.webp", "Multi-Bank Syndicated EMI Suite", "Instant Escrow & Lowest APR Clearance", (20, 35, 25), (45, 85, 60))
]
for filename, title, sub, c1, c2 in calcs:
    w, h = 600, 360
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=30, col=(255, 255, 255, 20))
    pts = [(60, 240), (140, 220), (220, 180), (300, 190), (380, 130), (460, 140), (540, 80)]
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=(245, 158, 11), width=4)
    for p in pts:
        draw.ellipse([(p[0]-5, p[1]-5), (p[0]+5, p[1]+5)], fill=(255, 255, 255), outline=(245, 158, 11), width=2)
    draw.rounded_rectangle([(30, h - 85), (w - 30, h - 20)], radius=12, fill=(15, 23, 42))
    draw.text((50, h - 72), title, fill=(255, 255, 255), font=font_md)
    draw.text((50, h - 45), f">> {sub}", fill=(52, 211, 153), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 6. DEVELOPERS
# ==========================================================
devs = [
    ("dev-godrej.webp", "GODREJ PROPERTIES", "Tier-1 Certified Partner", (20, 30, 45)),
    ("dev-prestige.webp", "PRESTIGE GROUP", "Commercial & Residential Partner", (35, 20, 30)),
    ("dev-brigade.webp", "BRIGADE ENTERPRISES", "Tech Park Partner", (15, 35, 30)),
    ("dev-casagrand.webp", "CASAGRAND BUILDERS", "Gated Township Partner", (30, 25, 15)),
    ("dev-sobha.webp", "SOBHA LIMITED", "Super Luxury Partner", (25, 15, 40)),
    ("dev-puravankara.webp", "PURAVANKARA LIMITED", "Contemporary Habitats", (40, 20, 20))
]
for filename, name, tag, col in devs:
    w, h = 400, 240
    img = create_gradient(w, h, col, (col[0]+30, col[1]+30, col[2]+30))
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=25, col=(255, 255, 255, 18))
    draw.rounded_rectangle([(w//2 - 50, 40), (w//2 + 50, 120)], radius=14, fill=(15, 23, 42), outline=(245, 158, 11), width=2)
    draw.text((w//2 - 25, 65), name[:2], fill=(245, 158, 11), font=font_lg)
    draw.rounded_rectangle([(20, h - 80), (w - 20, h - 20)], radius=10, fill=(15, 23, 42))
    draw.text((35, h - 68), name, fill=(255, 255, 255), font=font_md)
    draw.text((35, h - 42), f"* {tag} | Direct Mandate", fill=(245, 158, 11), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 7. ADVISORY PROCESS
# ==========================================================
processes = [
    ("proc-audit.webp", "Stage 1: 120-Point Title Audit", "High Court Senior Counsel Deed Examination", (25, 12, 45), (60, 25, 95)),
    ("proc-inspection.webp", "Stage 2: Drone & Structural Quality Audit", "Foundation, Concrete & Environmental Clearance", (14, 28, 50), (30, 70, 110)),
    ("proc-negotiation.webp", "Stage 3: Institutional Price Underwriting", "Direct-from-Developer Zero Brokerage Terms", (32, 22, 12), (75, 55, 25)),
    ("proc-escrow.webp", "Stage 4: Bank Escrow & Digital Handover", "Encumbrance-Free Key Registration & Possession", (15, 35, 25), (35, 80, 55))
]
for filename, title, sub, c1, c2 in processes:
    w, h = 500, 320
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=30, col=(255, 255, 255, 18))
    draw.ellipse([(w//2 - 40, 50), (w//2 + 40, 130)], fill=(245, 158, 11))
    draw.text((w//2 - 15, 75), "OK", fill=(15, 23, 42), font=font_lg)
    draw.rounded_rectangle([(20, h - 90), (w - 20, h - 20)], radius=12, fill=(15, 23, 42))
    draw.text((35, h - 75), title, fill=(255, 255, 255), font=font_md)
    draw.text((35, h - 45), sub, fill=(245, 158, 11), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 8. MARKET INTEL & PROPTECH TELEMETRY
# ==========================================================
intel_items = [
    ("intel-market-growth.webp", "2026 Micro-Market Appreciation Index", "Salem, Coimbatore & Chennai Expressways", (18, 12, 40), (45, 25, 85)),
    ("intel-rental-yield.webp", "Commercial vs Residential Yield Benchmarks", "High Court & Tech Corridors Telemetry", (12, 26, 44), (28, 65, 100)),
    ("intel-rera-telemetry.webp", "RERA 2.0 Digital Compliance Matrix", "Automated Municipal Registry Scrutiny", (25, 30, 15), (60, 75, 35))
]
for filename, title, sub, c1, c2 in intel_items:
    w, h = 560, 340
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=28, col=(255, 255, 255, 16))
    bars = [(70, 110), (130, 150), (190, 95), (250, 180), (310, 140), (370, 210), (430, 165), (490, 230)]
    for bx, bh in bars:
        draw.rectangle([(bx, 240 - bh), (bx + 35, 240)], fill=(245, 158, 11), outline=(255, 255, 255), width=1)
    draw.rounded_rectangle([(20, h - 85), (w - 20, h - 18)], radius=12, fill=(15, 23, 42))
    draw.text((35, h - 72), title, fill=(255, 255, 255), font=font_md)
    draw.text((35, h - 45), f">> {sub}", fill=(52, 211, 153), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 9. AVATARS & TESTIMONIAL CLIENTS
# ==========================================================
avatars = [
    ("avatar-karthik.webp", "Karthik Raja", "VP at Global Tech (Dubai)", (20, 25, 45)),
    ("avatar-radhika.webp", "Dr. Radhika Sharma", "Chief Pediatric Surgeon", (40, 15, 35)),
    ("avatar-venkat.webp", "Venkatesh Murugan", "Industrialist (Salem-Coimbatore)", (15, 35, 28)),
    ("avatar-ananya.webp", "Shilpa & Rajesh", "HNW Villa Owners", (35, 22, 15)),
    ("advisor-dr-shilpi.webp", "Dr. Shilpi Singh", "Senior Legal Counsel (High Court)", (30, 12, 48)),
    ("advisor-ananya-sen.webp", "Ananya Sen", "Commercial Valuation Specialist", (15, 30, 50)),
    ("advisor-meera-nair.webp", "Meera Nair", "Forensic Property Title Lead", (20, 38, 30)),
    ("advisor-priya-raman.webp", "Priya Raman", "Wealth & Escrow Director", (38, 20, 22))
]
for filename, name, role, col in avatars:
    w, h = 320, 320
    img = create_gradient(w, h, col, (col[0]+40, col[1]+40, col[2]+40))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(60, 40), (260, 240)], fill=(col[0]+20, col[1]+20, col[2]+20), outline=(245, 158, 11), width=4)
    draw.ellipse([(120, 70), (200, 150)], fill=(245, 158, 11))
    draw.polygon([(85, 230), (235, 230), (210, 160), (110, 160)], fill=(248, 250, 252))
    draw.rounded_rectangle([(15, h - 68), (w - 15, h - 14)], radius=8, fill=(15, 23, 42))
    draw.text((25, h - 58), name, fill=(255, 255, 255), font=font_md)
    draw.text((25, h - 36), role[:32], fill=(245, 158, 11), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 10. VIP CONCIERGE & EXPERIENCE CENTER
# ==========================================================
vip_items = [
    ("vip-lounge-interior.webp", "Salem VIP Investor Private Lounge", "Chauffeur Pickups & Private Deed Closings", (18, 10, 35), (45, 20, 75)),
    ("vip-consultation-chamber.webp", "Chamber 1 Executive Advisory Suite", "Dedicated High Court Legal & Financial Desk", (12, 24, 40), (28, 55, 90))
]
for filename, title, sub, c1, c2 in vip_items:
    w, h = 600, 360
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=30, col=(255, 255, 255, 18))
    draw.rectangle([(80, 80), (w - 80, 240)], fill=(c1[0]+22, c1[1]+22, c1[2]+25), outline=(245, 158, 11), width=2)
    draw.rounded_rectangle([(140, 140), (w - 140, 210)], radius=15, fill=(245, 158, 11))
    draw.rounded_rectangle([(30, h - 85), (w - 30, h - 20)], radius=12, fill=(15, 23, 42))
    draw.text((45, h - 72), title, fill=(255, 255, 255), font=font_md)
    draw.text((45, h - 45), f">> {sub}", fill=(245, 158, 11), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 11. ABOUT PAGE IMAGES
# ==========================================================
about_items = [
    ("about-headquarters.webp", "Stackly Salem Flagship Experience Center", "State-of-the-Art PropTech & Title Due Diligence Hub", (20, 10, 42), (52, 22, 90)),
    ("about-leadership-team.webp", "Executive Advisory Council", "Former High Court Advocates & Valuation Pioneers", (14, 25, 45), (32, 60, 105)),
    ("about-award-trophy.webp", "National Excellence in PropTech 2026", "Awarded No. 1 Certified Real Estate Consultancy", (35, 24, 12), (85, 60, 25)),
    ("about-rera-crest.webp", "Official 100% RERA Accreditation Seal", "Strict 120-Point Title Examination Guarantee", (15, 35, 25), (35, 85, 55)),
    ("about-vision-future.webp", "Vision 2030 PropTech Roadmap", "AI Driven Instant Escrow & Title Blockchain", (28, 15, 40), (68, 32, 90))
]
for filename, title, sub, c1, c2 in about_items:
    w, h = 600, 360
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=30, col=(255, 255, 255, 20))
    draw.ellipse([(w//2 - 55, 55), (w//2 + 55, 165)], fill=(min(255, c2[0]+25), min(255, c2[1]+25), min(255, c2[2]+25)), outline=(245, 158, 11), width=3)
    draw.text((w//2 - 25, 95), "STACKLY", fill=(245, 158, 11), font=font_tag)
    draw.rounded_rectangle([(30, h - 85), (w - 30, h - 20)], radius=12, fill=(15, 23, 42))
    draw.text((45, h - 72), title, fill=(255, 255, 255), font=font_md)
    draw.text((45, h - 45), f">> {sub}", fill=(245, 158, 11), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 12. SERVICES PAGE ASSETS
# ==========================================================
services_detail = [
    ("service-detail-residential.webp", "Residential Acquisition Suite", "Fairlands & OMR Gated Communities", (25, 12, 45), (65, 25, 95)),
    ("service-detail-commercial.webp", "Institutional Commercial & SCO", "MNC Pre-Leased Office Parks", (15, 30, 50), (32, 68, 110)),
    ("service-detail-nri.webp", "24/7 Global NRI Concierge Desk", "NRE/NRO Banking & Tax Repatriation", (35, 20, 20), (85, 42, 38)),
    ("service-detail-legal.webp", "120-Point High Court Title Audit", "Zero-Litigation Certified Assurance", (38, 24, 15), (90, 60, 28)),
    ("service-detail-homeloan.webp", "Multi-Bank Syndicated Mortgage", "SBI & HDFC Pre-Approved Interest Rates", (15, 35, 28), (38, 85, 60)),
    ("service-detail-portfolio.webp", "High-Net-Worth Portfolio Restructure", "Capital Gains 54F & 1031 Tax Shield", (28, 15, 42), (65, 35, 88))
]
for filename, title, sub, c1, c2 in services_detail:
    w, h = 540, 320
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=28, col=(255, 255, 255, 18))
    draw.polygon([(180, 150), (270, 100), (360, 150), (270, 200)], fill=(min(255, c2[0]+30), min(255, c2[1]+30), min(255, c2[2]+30)))
    draw.polygon([(180, 150), (270, 200), (270, 270), (180, 220)], fill=(min(255, c2[0]+15), min(255, c2[1]+15), min(255, c2[2]+15)))
    draw.polygon([(270, 200), (360, 150), (360, 220), (270, 270)], fill=(min(255, c2[0]+45), min(255, c2[1]+45), min(255, c2[2]+45)))
    draw.rounded_rectangle([(25, h - 80), (w - 25, h - 20)], radius=10, fill=(15, 23, 42))
    draw.text((42, h - 68), title, fill=(255, 255, 255), font=font_md)
    draw.text((42, h - 42), f"Verified Advisory Record: 100% >> {sub[:28]}", fill=(245, 158, 11), font=font_sm)
    save_webp(img, filename)

# ==========================================================
# 13. CONTACT PAGE ASSETS
# ==========================================================
contact_items = [
    ("contact-salem-center.webp", "Salem Central Experience Flagship", "Fairlands Main Road | Valet Parking & VIP Lounge", (18, 10, 38), (48, 22, 85)),
    ("contact-advisory-desk.webp", "Private Client Advisory Desks", "Meet Senior Legal Advocates & Wealth Advisors", (12, 25, 45), (28, 62, 105)),
    ("contact-meeting-room.webp", "High-Security Video Conference Room", "Encrypted Global NRI Video Escrow Closings", (30, 20, 15), (75, 50, 25))
]
for filename, title, sub, c1, c2 in contact_items:
    w, h = 600, 360
    img = create_gradient(w, h, c1, c2)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, w, h, step=30, col=(255, 255, 255, 20))
    draw.rectangle([(70, 70), (w - 70, 240)], fill=(c1[0]+22, c1[1]+22, c1[2]+25), outline=(245, 158, 11), width=2)
    draw.rounded_rectangle([(30, h - 85), (w - 30, h - 20)], radius=12, fill=(15, 23, 42))
    draw.text((45, h - 72), title, fill=(255, 255, 255), font=font_md)
    draw.text((45, h - 45), f">> {sub}", fill=(245, 158, 11), font=font_sm)
    save_webp(img, filename)

print("=== ALL WEBP IMAGES GENERATED AND VALIDATED UNDER 100KB ===")
