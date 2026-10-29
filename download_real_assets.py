import os
import io
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

OUT_DIR = os.path.join('assets', 'images')
os.makedirs(OUT_DIR, exist_ok=True)

# 100% UNIQUE, DISTINCT Unsplash Photo IDs for EVERY SINGLE asset (ZERO DUPLICATES!)
IMAGE_SOURCES = {
    # Hero Slides (Each has a completely distinct panoramic view)
    'hero-slide-1.webp': ('photo-1545324418-cc1a3fa10c00', 1200, 680),  # Luxury residential high-rise at dusk
    'hero-slide-2.webp': ('photo-1613977257363-707ba9348227', 1200, 680),  # Ultra modern villa with illuminated pool
    'hero-slide-3.webp': ('photo-1486406146926-c627a92ad1ab', 1200, 680),  # Commercial glass skyscraper reaching sky
    'hero-slide-4.webp': ('photo-1600585154340-be6161a56a0c', 1200, 680),  # Contemporary architectural garden estate
    'hero-slide-5.webp': ('photo-1600607687939-ce8a6c25118c', 1200, 680),  # Penthouse lounge with skyline windows
    'hero-estate-banner.webp': ('photo-1600596542815-ffad4c1539a9', 1200, 680),  # Grand villa with manicured lawn

    # Property Categories (Distinct category representations)
    'cat-villas.webp': ('photo-1580587771525-78b9dba3b914', 600, 420),      # Classic luxury villa
    'cat-apartments.webp': ('photo-1515263487990-61b07816b324', 600, 420),  # Modern residential apartment building
    'cat-commercial.webp': ('photo-1497366216548-37526070297c', 600, 420),  # Premium corporate open-plan office
    'cat-plots.webp': ('photo-1500382017468-9049fed747ef', 600, 420),       # Open green investment plots
    'cat-penthouses.webp': ('photo-1512917774080-9991f1c4c750', 600, 420),  # Luxury rooftop terrace penthouse
    'cat-farmhouses.webp': ('photo-1518780664697-55e3ad937233', 600, 420),  # Serene pastoral estate farmhouse

    # Localities (Distinct geographic / architectural looks)
    'loc-fairlands.webp': ('photo-1600565193348-f74bd3c7ccdf', 600, 420),    # Fairlands luxury avenue
    'loc-alagapuram.webp': ('photo-1570129477492-45c003edd2be', 600, 420),   # Alagapuram residential street
    'loc-hasthampatti.webp': ('photo-1600585154526-990dced4db0d', 600, 420), # Hasthampatti grand estate
    'loc-suramangalam.webp': ('photo-1448630360428-65456885c650', 600, 420), # Suramangalam city junction
    'loc-yercaud.webp': ('photo-1506744038136-46273834b3fb', 600, 420),      # Yercaud misty green hillstation
    'loc-omr-chennai.webp': ('photo-1477959858617-67f30bc75b82', 600, 420),  # OMR Chennai illuminated IT expressway

    # Featured Projects (Each project card has a 100% unique design)
    'proj-aurora-residences.webp': ('photo-1567496898669-ee935f5f647a', 640, 440), # Aurora: High-end geometric apartments
    'proj-zenith-tower.webp': ('photo-1577495508048-b635879837f1', 640, 440),      # Zenith: Diagonal glass skyscraper
    'proj-elysium-penthouse.webp': ('photo-1600607687920-4e2a09cf159d', 640, 440), # Elysium: Sunset sky penthouse
    'proj-verdant-gardens.webp': ('photo-1600566753376-12c8ab7fb75b', 640, 440),   # Verdant: Warm landscaped community
    'proj-serene-villas.webp': ('photo-1600585154363-67eb9e2e2099', 640, 440),     # Serene: Minimalist architectural villa
    'proj-solaris-estates.webp': ('photo-1600573472591-ee6b68d14c68', 640, 440),   # Solaris: Elegant courtyard residence
    'proj-signature-arcade.webp': ('photo-1555636222-cae831e670b3', 640, 440),    # Signature: Retail commercial complex
    'project-luxury-villa.webp': ('photo-1584622650111-993a426fbf0a', 640, 440),    # Luxury Villa: White contemporary mansion
    'project-skyline-tower.webp': ('photo-1542314831-068cd1dbfeeb', 640, 440),     # Skyline Tower: Prestige high-rise
    'project-commercial-park.webp': ('photo-1507679799987-c73779587ccf', 640, 440),  # Commercial Park: IT glass park
    'project-eco-township.webp': ('photo-1500530855697-b586d89ba3ee', 640, 440),   # Eco Township: Open green acreage
    'project-penthouse.webp': ('photo-1502672260266-1c1ef2d93688', 640, 440),       # Penthouse: Chic loft interior

    # Top Developers (Each developer brand has distinct landmark architecture)
    'dev-godrej.webp': ('photo-1574362848149-11496d93a7c7', 600, 380),     # Godrej: Sleek modern residential tower
    'dev-prestige.webp': ('photo-1554469384-e58fac16e23a', 600, 380),      # Prestige: Curving reflective commercial glass
    'dev-brigade.webp': ('photo-1479839672679-a46483c0e7c8', 600, 380),       # Brigade: Futuristic retail & tech hub
    'dev-casagrand.webp': ('photo-1512915922686-57c11dde9b6b', 600, 380),     # Casagrand: Mediterranean community estate
    'dev-sobha.webp': ('photo-1600585152220-90363fe7e115', 600, 380),         # Sobha: Super luxury villa craftsmanship
    'dev-puravankara.webp': ('photo-1460317442991-0ec209397118', 600, 380),   # Puravankara: Elegant high-rise balconies

    # Advisory Process Steps
    'proc-audit.webp': ('photo-1450133064473-71024230f91b', 600, 400),       # Legal title deed & fountain pen
    'proc-inspection.webp': ('photo-1504307651254-35680f356dfd', 600, 400),  # Architect blueprint inspection
    'proc-negotiation.webp': ('photo-1557804506-669a67965ba0', 600, 400),   # Executive boardroom deal consultation
    'proc-escrow.webp': ('photo-1554224155-8d04cb21cd6c', 600, 400),        # RERA financial escrow document

    # Market Telemetry & Intelligence Screens
    'intel-market-growth.webp': ('photo-1611974789855-9c2a0a7236a3', 600, 400), # Financial real estate index screen
    'intel-rental-yield.webp': ('photo-1551288049-bebda4e38f71', 600, 400),  # Computerized telemetry dashboard
    'intel-rera-telemetry.webp': ('photo-1460925895917-afdab827c52f', 600, 400), # RERA due diligence analytics chart
    'market-chart-2026.webp': ('photo-1590283603385-17ffb3a7f29f', 600, 400),   # 2026 appreciation forecast chart
    'calc-roi-visual.webp': ('photo-1554224154-26032ffc0d07', 600, 400),      # ROI financial calculation spreadsheet
    'calc-mortgage-visual.webp': ('photo-1560518883-ce09059eeffa', 600, 400), # House key handover with bank contract

    # Portraits (Unique professional advisor and client headshots)
    'advisor-dr-shilpi.webp': ('photo-1573496359142-b8d87734a5a2', 400, 400),
    'advisor-ananya-sen.webp': ('photo-1580894732444-8ecded7900cd', 400, 400),
    'advisor-meera-nair.webp': ('photo-1573497019940-1c28c88b4f3e', 400, 400),
    'advisor-priya-raman.webp': ('photo-1573496799652-408c2ac9fe98', 400, 400),
    'advisor-priya.webp': ('photo-1598550874175-4d0ef436c909', 400, 400),
    'advisor-shilpi.webp': ('photo-1573497491208-6b1acb260507', 400, 400),
    'advisor-ananya.webp': ('photo-1531497865144-0464ef8fb9a9', 400, 400),
    'advisor-meera.webp': ('photo-1551836022-d5d88e9218df', 400, 400),
    'avatar-1.webp': ('photo-1560250097-0b93528c311a', 400, 400),
    'avatar-radhika.webp': ('photo-1534528741775-53994a69daeb', 400, 400),
    'avatar-karthik.webp': ('photo-1507003211169-0a1dd7228f2d', 400, 400),
    'avatar-venkat.webp': ('photo-1500648767791-00dcc994a43e', 400, 400),
    'avatar-ananya.webp': ('photo-1544005313-94ddf0286df2', 400, 400),

    # Corporate & About Page Facilities
    'about-headquarters.webp': ('photo-1497366811353-6870744d04b2', 800, 520), # Modern glass HQ atrium
    'about-leadership-team.webp': ('photo-1522071820081-009f0129c71c', 800, 520), # Advisory team around conference table
    'about-vision-future.webp': ('photo-1519501025264-65ba15a82390', 800, 520), # Architectural landmark vision
    'about-rera-crest.webp': ('photo-1589829545856-d10d557cf95f', 600, 400),   # Legal gavel & High Court statute seal
    'about-award-trophy.webp': ('photo-1567427017947-545c5f8d16ad', 600, 400), # Real gold excellence award trophy

    # Services (Distinct architectural illustrations)
    'service-residential.webp': ('photo-1600210492486-724fe5c67fb0', 600, 400), # Residential luxury exterior
    'service-commercial.webp': ('photo-1497215842964-222b430dc094', 600, 400),  # Commercial glass park
    'service-legal.webp': ('photo-1521791136064-7986c2920216', 600, 400),       # High Court legal audit
    'service-homeloan.webp': ('photo-1560520653-9e0e4c89eb11', 600, 400),    # Preferential mortgage rate desk
    'service-nri.webp': ('photo-1436491865332-7a61a109cc05', 600, 400),         # NRI international corridor
    'service-portfolio.webp': ('photo-1526304640581-d334cdbbf45e', 600, 400),   # Portfolio return on equity
    'service-detail-residential.webp': ('photo-1600566753190-17f0baa2a6c3', 800, 500),
    'service-detail-commercial.webp': ('photo-1508873696983-2df5293cb32f', 800, 500),
    'service-detail-legal.webp': ('photo-1505664194779-8beaceb93744', 800, 500),
    'service-detail-homeloan.webp': ('photo-1554224155-6726b3ff858f', 800, 500),
    'service-detail-nri.webp': ('photo-1512453979798-5ea266f8880c', 800, 500), # Dubai skyline for NRI detail
    'service-detail-portfolio.webp': ('photo-1543286386-713bdd548da4', 800, 500),

    # Blog Covers (All 6 blog posts have completely unique imagery)
    'blog-rera-guide.webp': ('photo-1453728013993-6d66e9c9123a', 700, 450),      # Legal RERA guide
    'blog-cover-1.webp': ('photo-1434030216411-0b793f4b4173', 700, 450),         # Title verification audit
    'blog-nri-investment.webp': ('photo-1525625293386-3f8f99389edd', 700, 450),  # NRI Global corridor
    'blog-cover-2.webp': ('photo-1506973035872-a4ec16b8e8d9', 700, 450),         # Cross border investment
    'blog-luxury-villas.webp': ('photo-1600607687644-c7171b42498b', 700, 450),   # Yercaud luxury villas
    'blog-cover-3.webp': ('photo-1600566752355-35792bedcfea', 700, 450),         # Ultra-luxury estates
    'blog-proptech-ai.webp': ('photo-1518770660439-4636190af475', 700, 450),     # AI PropTech technology chip/data
    'blog-cover-4.webp': ('photo-1451187580459-43490279c0fa', 700, 450),         # Global satellite connectivity
    'blog-emerging-corridors.webp': ('photo-1506146332389-18140dc7b2fb', 700, 450), # Salem-Bengaluru highway
    'blog-tax-reit.webp': ('photo-1559526324-4b87b5e36e44', 700, 450),          # REIT tax optimization

    # Contact & VIP Experience Desks
    'contact-salem-center.webp': ('photo-1524758631624-e2822e304c36', 700, 450),
    'contact-meeting-room.webp': ('photo-1497366754035-f200968a6e72', 700, 450),
    'contact-advisory-desk.webp': ('photo-1497215728101-856f4ea42174', 700, 450),
    'vip-consultation-chamber.webp': ('photo-1618221195710-dd6b41faaea6', 700, 450),
    'vip-lounge-interior.webp': ('photo-1618219908412-a29a1bb7b86e', 700, 450),
    'login-chart-banner.webp': ('photo-1551836022-4c4c79ecde51', 800, 260),
}

# Verify uniqueness
pids = [v[0] for v in IMAGE_SOURCES.values()]
assert len(pids) == len(set(pids)), f"Duplicate detected! {len(pids)} != {len(set(pids))}"
print(f"Verified: All {len(IMAGE_SOURCES)} assets have 100% UNIQUE photo IDs!")

def process_image(item):
    filename, (photo_id, target_w, target_h) = item
    out_path = os.path.join(OUT_DIR, filename)
    url = f"https://images.unsplash.com/{photo_id}?w={target_w}&h={target_h}&fit=crop&crop=entropy&q=80"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        
        img = Image.open(io.BytesIO(data)).convert('RGB')
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        quality = 82
        while quality > 40:
            buf = io.BytesIO()
            img.save(buf, format='WEBP', quality=quality, method=6)
            size = buf.tell()
            if size <= 95 * 1024:
                break
            quality -= 6
            
        with open(out_path, 'wb') as f:
            f.write(buf.getvalue())
            
        file_size_kb = os.path.getsize(out_path) / 1024
        print(f"[OK] {filename:32} -> {file_size_kb:.1f} KB (quality={quality})")
        return True
    except Exception as e:
        print(f"[FAIL] {filename}: {e}")
        return False

if __name__ == '__main__':
    print(f"Starting download of {len(IMAGE_SOURCES)} 100% unique photos from Unsplash...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_image, IMAGE_SOURCES.items()))

    success = sum(1 for r in results if r)
    print(f"\nAll Done! Successfully downloaded {success}/{len(IMAGE_SOURCES)} unique real estate images!")
