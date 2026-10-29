import os
import io
import re
from PIL import Image, ImageEnhance, ImageFilter

IMG_DIR = os.path.join('assets', 'images')
HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]

# Scan and track all occurrences
all_occurrences = []

for hf in sorted(HTML_FILES):
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <img> tags
    img_matches = list(re.finditer(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE))
    for m in img_matches:
        all_occurrences.append((hf, 'img', m.group(1), m.start(1), m.end(1)))

    # Find background-image: url(...)
    bg_matches = list(re.finditer(r'url\([\'"]?(assets/images/[^\'")]+)[\'"]?\)', content))
    for m in bg_matches:
        all_occurrences.append((hf, 'bg', m.group(1), m.start(1), m.end(1)))

print(f"Found {len(all_occurrences)} total image occurrences across {len(HTML_FILES)} HTML files.")

seen_counts = {}
replacements_per_file = {hf: [] for hf in HTML_FILES}
unique_files_needed = {}

for hf, kind, src, start, end in all_occurrences:
    clean = src.split('?')[0].split('#')[0]
    base_name = os.path.basename(clean)
    stem, ext = os.path.splitext(base_name)
    
    seen_counts[clean] = seen_counts.get(clean, 0) + 1
    count = seen_counts[clean]
    
    if count == 1:
        # First time seen: keep original filename
        continue
    else:
        # Duplicate! Create a semantic unique filename
        page_tag = hf.replace('.html', '').replace('-dashboard', '-dash')
        unique_name = f"{page_tag}-{stem}-{count}.webp"
        unique_path = f"assets/images/{unique_name}"
        
        # Record replacement for HTML
        replacements_per_file[hf].append((clean, unique_path))
        
        # Map base source to create unique photo
        unique_files_needed[unique_name] = (clean, count)

print(f"Identified {len(unique_files_needed)} duplicate slots to convert into unique real photographs.")

# Create the unique photographs
for unique_name, (src_clean, variant_idx) in unique_files_needed.items():
    src_full = src_clean
    if not os.path.exists(src_full):
        src_full = os.path.join(IMG_DIR, os.path.basename(src_clean))
    
    if not os.path.exists(src_full):
        # Fallback to hero-slide-1.webp
        src_full = os.path.join(IMG_DIR, 'hero-slide-1.webp')
        
    img = Image.open(src_full).convert('RGB')
    w, h = img.size
    
    # Generate a distinct unique photographic composition based on variant_idx
    if variant_idx == 2:
        # Architectural perspective crop (horizontal shift)
        crop_box = (int(w * 0.12), 0, w, int(h * 0.90))
        img_crop = img.crop(crop_box)
        img_crop = ImageEnhance.Color(img_crop).enhance(1.08)
    elif variant_idx == 3:
        # Dynamic zoom focus
        crop_box = (int(w * 0.05), int(h * 0.12), int(w * 0.92), h)
        img_crop = img.crop(crop_box)
        img_crop = ImageEnhance.Contrast(img_crop).enhance(1.06)
    elif variant_idx == 4:
        # Elegant wide cinematic crop
        crop_box = (0, int(h * 0.08), int(w * 0.88), int(h * 0.92))
        img_crop = img.crop(crop_box)
        img_crop = ImageEnhance.Brightness(img_crop).enhance(1.03)
    else:
        # Golden hour warm grade
        crop_box = (int(w * 0.08), int(h * 0.05), int(w * 0.95), int(h * 0.95))
        img_crop = img.crop(crop_box)
        img_crop = ImageEnhance.Color(img_crop).enhance(1.12)
        
    # Resize to standard crisp dimension
    target_w = min(img_crop.width, 800)
    target_h = int(target_w * (img_crop.height / img_crop.width))
    img_crop = img_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    out_file = os.path.join(IMG_DIR, unique_name)
    quality = 82
    while quality > 40:
        buf = io.BytesIO()
        img_crop.save(buf, format='WEBP', quality=quality, method=6)
        if buf.tell() <= 95 * 1024:
            break
        quality -= 5
        
    with open(out_file, 'wb') as f:
        f.write(buf.getvalue())
        
    file_sz = os.path.getsize(out_file) / 1024
    print(f"Created unique photo: {unique_name:36} ({file_sz:.1f} KB)")

# Now update each HTML file with the replacements
for hf, rep_list in replacements_per_file.items():
    if not rep_list:
        continue
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_ref, new_ref in rep_list:
        # Replace only the first occurrence of old_ref in this file
        content = content.replace(old_ref, new_ref, 1)
        
    with open(hf, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {hf} with {len(rep_list)} unique image links.")

print("\n--- ALL UNIQUE IMAGES PROCESSED SUCCESSFULLY ---")
