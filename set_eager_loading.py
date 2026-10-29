import os

for hf in [f for f in os.listdir('.') if f.endswith('.html')]:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'loading="lazy"' in content:
        content = content.replace('loading="lazy"', 'loading="eager"')
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {hf} to eager loading.")
