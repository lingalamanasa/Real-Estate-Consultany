import os
import re
from bs4 import BeautifulSoup
from collections import defaultdict

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

img_usage = defaultdict(list)
all_refs = []

for hf in sorted(html_files):
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and not src.startswith('http'):
            clean = src.split('?')[0].split('#')[0]
            img_usage[clean].append(hf)
            all_refs.append(clean)
    
    # Check background-image in styles
    bgs = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', content)
    for bg in bgs:
        if bg.startswith('assets/images/'):
            clean = bg.split('?')[0].split('#')[0]
            img_usage[clean].append(hf + ' (bg)')
            all_refs.append(clean)

print(f"Total image references in website: {len(all_refs)}")
print(f"Distinct image filenames referenced: {len(img_usage)}")

duplicates = {k: v for k, v in img_usage.items() if len(v) > 1}
print(f"\nNumber of images referenced more than once: {len(duplicates)}")
for k, v in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"  {k:38} used {len(v)} times in: {v}")
