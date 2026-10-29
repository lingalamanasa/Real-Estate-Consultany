import os
import io
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from bs4 import BeautifulSoup
from collections import defaultdict

OUT_DIR = os.path.join('assets', 'images')
os.makedirs(OUT_DIR, exist_ok=True)

# Curated list of distinct, valid Unsplash photography photo IDs (real estate, architecture, interiors, portraits, analytics)
UNIQUE_PHOTO_SPECS = {
    # index.html hero background slides (unique from foreground slider)
    'index-hero-bg-1.webp': ('photo-1545324418-cc1a3fa10c00', 1200, 700), # Skyline high-rise
    'index-hero-bg-2.webp': ('photo-1613977257363-707ba9348227', 1200, 700), # Luxury villa pool
    'index-hero-bg-3.webp': ('photo-1486406146926-c627a92ad1ab', 1200, 700), # Commercial skyscraper
    'index-hero-bg-4.webp': ('photo-1600585154340-be6161a56a0c', 1200, 700), # Gated estate
    'index-hero-bg-5.webp': ('photo-1600607687939-ce8a6c25118c', 1200, 700), # Luxury penthouse terrace
    'index-vip-chamber.webp': ('photo-1600210492486-724fe5c67fb0', 700, 450), # High-end private chamber
    'index-vip-lounge.webp': ('photo-1600585154363-67eb9e2e2099', 700, 450),  # Luxury lounge interior
    'modal-auth-banner.webp': ('photo-1551288049-bebda4e38f71', 800, 260),

    # about.html unique images
    'about-hero-bg-1.webp': ('photo-1497366811353-6870744d04b2', 1200, 700), # Corporate headquarters
    'about-hero-bg-2.webp': ('photo-1486406146926-c627a92ad1ab', 1200, 700), # Vision tower
    'about-hero-bg-3.webp': ('photo-1522071820081-009f0129c71c', 1200, 700), # Leadership council
    'about-hero-bg-4.webp': ('photo-1545324418-cc1a3fa10c00', 1200, 700), # Modern glass architecture
    'about-proc-audit.webp': ('photo-1450133064473-71024230f91b', 600, 400), # Due diligence audit
    'about-proc-inspection.webp': ('photo-1504307651254-35680f356dfd', 600, 400), # Site inspection engineer
    'about-proc-escrow.webp': ('photo-1554224155-8d04cb21cd6c', 600, 400), # Financial escrow
    'about-trophy-excellence.webp': ('photo-1567427017947-545c5f8d16ad', 600, 400), # Award trophy
    'about-rera-crest-seal.webp': ('photo-1589829545856-d10d557cf95f', 600, 400), # Legal seal
    'about-roi-visual.webp': ('photo-1554224154-26032ffc0d07', 600, 400), # Financial plan
    'about-market-growth.webp': ('photo-1611974789855-9c2a0a7236a3', 600, 400), # Market growth
    'about-login-banner.webp': ('photo-1551288049-bebda4e38f71', 800, 260),
    'about-service-legal.webp': ('photo-1450133064473-71024230f91b', 600, 400),
    'about-service-portfolio.webp': ('photo-1551288049-bebda4e38f71', 600, 400),
    'about-verdant-estate.webp': ('photo-1600585154340-be6161a56a0c', 640, 440),

    # services.html unique images
    'services-hero-bg-1.webp': ('photo-1497366216548-37526070297c', 1200, 700), # Corporate office
    'services-hero-bg-2.webp': ('photo-1600585154340-be6161a56a0c', 1200, 700), # Luxury residential
    'services-hero-bg-3.webp': ('photo-1486406146926-c627a92ad1ab', 1200, 700), # Commercial tech
    'services-hero-bg-4.webp': ('photo-1600607687939-ce8a6c25118c', 1200, 700), # VIP private chamber
    'services-hero-residential.webp': ('photo-1580587771525-78b9dba3b914', 600, 400), # Residential desk
    'services-hero-commercial.webp': ('photo-1497366216548-37526070297c', 600, 400),  # Commercial desk
    'services-hero-nri.webp': ('photo-1436491865332-7a61a109cc05', 600, 400),         # NRI desk
    'services-market-chart.webp': ('photo-1611974789855-9c2a0a7236a3', 600, 400),     # Yield analytics
    'services-penthouse.webp': ('photo-1512917774080-9991f1c4c750', 600, 400),        # Sky penthouse
    'services-vip-lounge.webp': ('photo-1600585154526-990dced4db0d', 700, 450),       # VIP lounge
    'services-vip-chamber.webp': ('photo-1600607687920-4e2a09cf159d', 700, 450),      # VIP chamber

    # blog.html unique images
    'blog-hero-bg-1.webp': ('photo-1613977257363-707ba9348227', 1200, 700), # Twilight villa
    'blog-hero-bg-2.webp': ('photo-1486406146926-c627a92ad1ab', 1200, 700), # PropTech city
    'blog-hero-bg-3.webp': ('photo-1600585154340-be6161a56a0c', 1200, 700), # Eco township
    'blog-hero-bg-4.webp': ('photo-1448630360428-65456885c650', 1200, 700), # Expressway corridor
    'blog-roi-visual.webp': ('photo-1554224154-26032ffc0d07', 600, 400),
    'blog-rental-yield.webp': ('photo-1551288049-bebda4e38f71', 600, 400),
    'blog-market-chart.webp': ('photo-1611974789855-9c2a0a7236a3', 600, 400),
    'blog-vision-future.webp': ('photo-1486406146926-c627a92ad1ab', 600, 400),

    # contact.html unique images
    'contact-hero-bg-1.webp': ('photo-1497366811353-6870744d04b2', 1200, 700), # Salem Center
    'contact-hero-bg-2.webp': ('photo-1497366754035-f200968a6e72', 1200, 700), # Glass boardroom
    'contact-hero-bg-3.webp': ('photo-1600585154526-990dced4db0d', 1200, 700), # VIP lounge
    'contact-hero-bg-4.webp': ('photo-1497215728101-856f4ea42174', 1200, 700), # Consulting desk
    'contact-center-exterior.webp': ('photo-1486406146926-c627a92ad1ab', 700, 450), # Salem exterior
    'contact-meeting-suite.webp': ('photo-1497366754035-f200968a6e72', 700, 450),   # Meeting room
    'contact-advisory-room.webp': ('photo-1497215728101-856f4ea42174', 700, 450),   # Advisory room
    'contact-vip-lounge.webp': ('photo-1600585154526-990dced4db0d', 700, 450),      # VIP room
    'contact-proc-audit.webp': ('photo-1450133064473-71024230f91b', 600, 400),
    'contact-rera-crest.webp': ('photo-1589829545856-d10d557cf95f', 600, 400),
    'contact-zenith-tower.webp': ('photo-1486406146926-c627a92ad1ab', 600, 400),
    'contact-loc-fairlands.webp': ('photo-1564013799919-ab600027ffc6', 600, 400),
    'contact-loc-omr.webp': ('photo-1519501025264-65ba15a82390', 600, 400),
    'contact-dev-godrej.webp': ('photo-1545324418-cc1a3fa10c00', 600, 380),
    'contact-dev-prestige.webp': ('photo-1486406146926-c627a92ad1ab', 600, 380),
    'contact-dev-casagrand.webp': ('photo-1600585154340-be6161a56a0c', 600, 380),
    'contact-service-nri.webp': ('photo-1436491865332-7a61a109cc05', 600, 400),

    # user-dashboard.html unique images
    'dash-proc-audit.webp': ('photo-1450133064473-71024230f91b', 600, 400),
    'dash-proc-inspection.webp': ('photo-1504307651254-35680f356dfd', 600, 400),
    'dash-proc-escrow.webp': ('photo-1554224155-8d04cb21cd6c', 600, 400),
    'dash-rera-crest.webp': ('photo-1589829545856-d10d557cf95f', 600, 400),
    'dash-rera-seal.webp': ('photo-1450133064473-71024230f91b', 600, 400),
    'dash-roi-visual.webp': ('photo-1554224154-26032ffc0d07', 600, 400),
    'dash-mortgage-visual.webp': ('photo-1560518883-ce09059eeffa', 600, 400),
    'dash-market-growth.webp': ('photo-1611974789855-9c2a0a7236a3', 600, 400),
    'dash-rental-yield.webp': ('photo-1551288049-bebda4e38f71', 600, 400),
    'dash-advisor-shilpi.webp': ('photo-1573496359142-b8d87734a5a2', 400, 400),
    'dash-advisor-shilpi-sq.webp': ('photo-1573496359142-b8d87734a5a2', 400, 400),
    'dash-proj-aurora.webp': ('photo-1545324418-cc1a3fa10c00', 600, 400),
    'dash-proj-zenith.webp': ('photo-1486406146926-c627a92ad1ab', 600, 400),
    'dash-advisory-desk.webp': ('photo-1497215728101-856f4ea42174', 600, 400),

    # admin-dashboard.html unique images
    'admin-rera-seal.webp': ('photo-1589829545856-d10d557cf95f', 600, 400),
    'admin-market-growth.webp': ('photo-1611974789855-9c2a0a7236a3', 600, 400),
    'admin-rental-yield.webp': ('photo-1551288049-bebda4e38f71', 600, 400),
    'admin-market-chart.webp': ('photo-1551288049-bebda4e38f71', 600, 400),
    'admin-mortgage-visual.webp': ('photo-1560518883-ce09059eeffa', 600, 400),
    'admin-advisor-shilpi.webp': ('photo-1573496359142-b8d87734a5a2', 400, 400),
    'admin-advisor-ananya.webp': ('photo-1580894732444-8ecded7900cd', 400, 400),
    'admin-advisor-meera.webp': ('photo-1573497019940-1c28c88b4f3e', 400, 400),
    'admin-proj-aurora.webp': ('photo-1545324418-cc1a3fa10c00', 600, 400),
    'admin-proj-zenith.webp': ('photo-1486406146926-c627a92ad1ab', 600, 400),
    'admin-loc-yercaud.webp': ('photo-1506744038136-46273834b3fb', 600, 400),
    'admin-salem-center.webp': ('photo-1497366811353-6870744d04b2', 600, 400),
    'admin-dev-godrej.webp': ('photo-1545324418-cc1a3fa10c00', 600, 380),
    'admin-dev-prestige.webp': ('photo-1486406146926-c627a92ad1ab', 600, 380),
    'admin-dev-casagrand.webp': ('photo-1600585154340-be6161a56a0c', 600, 380),

    # signup.html
    'signup-chart-banner.webp': ('photo-1551288049-bebda4e38f71', 800, 260),
}

def download_and_save_webp(item):
    filename, (photo_id, target_w, target_h) = item
    out_path = os.path.join(OUT_DIR, filename)
    url = f"https://images.unsplash.com/{photo_id}?w={target_w}&h={target_h}&fit=crop&crop=entropy&q=80"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data)).convert('RGB')
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        quality = 82
        while quality > 40:
            buf = io.BytesIO()
            img.save(buf, format='WEBP', quality=quality, method=6)
            if buf.tell() <= 95 * 1024:
                break
            quality -= 6
            
        with open(out_path, 'wb') as f:
            f.write(buf.getvalue())
            
        print(f"[OK] {filename:32} -> {os.path.getsize(out_path)/1024:.1f} KB")
        return True
    except Exception as e:
        print(f"[FAIL] {filename}: {e}")
        return False

if __name__ == '__main__':
    print(f"Starting concurrent download of {len(UNIQUE_PHOTO_SPECS)} new unique images...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(download_and_save_webp, UNIQUE_PHOTO_SPECS.items()))
    print(f"Finished downloads! Success: {sum(1 for r in results if r)}/{len(UNIQUE_PHOTO_SPECS)}")
