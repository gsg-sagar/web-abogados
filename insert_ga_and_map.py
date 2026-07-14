import os
import re

# Configuration
GA_ID = "G-G9FR5QJT3P"
GA_SNIPPET = f"""
<script async src=\"https://www.googletagmanager.com/gtag/js?id={GA_ID}\"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{GA_ID}');
</script>
"""

# New Google Maps URL to use in schema.org hasMap
NEW_MAP_URL = "https://www.google.com/maps/place/Saval+Garc%C3%ADa+Abogados+%7C+Asesor%C3%ADa+jur%C3%ADdica+integral/@38.6495859,-0.122659,648m/data=!3m1!1e3!4m15!1m8!3m7!1s0xd62028317716699:0x3a9da8a15fad6dac!2sC.+Ram%C3%B3n+y+Cajal,+14,+03510+Callosa+de+Ensarri%C3%A1,+Alicante!3b1!8m2!3d38.6495859!4d-0.1200841!16s%2Fg%2F11c1dqcxpp!3m5!1s0xfddc866745052b9:0x5460d627fc071eb!8m2!3d38.6495875!4d-0.1200701!16s%2Fg%2F11wmtb5_7z?entry=ttu&g_ep=EgoyMDI2MDUxMy4wIKXMDSoASAFQAw%3D%3D"

def inject_ga(content):
    # Insert GA snippet before </head>
    if "</head>" in content:
        return content.replace("</head>", GA_SNIPPET + "\n</head>")
    return content

def update_map_url(content):
    # Replace any hasMap URL in JSON-LD blocks
    # Regex to find "hasMap":"..."
    pattern = r'(\"hasMap\":\")[^\"]+(\")'
    return re.sub(pattern, rf'\1{NEW_MAP_URL}\2', content)

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    content = inject_ga(content)
    content = update_map_url(content)
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    root = r"C:/Users/USUARIO/Documents/savalgarciabogados"
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith('.html'):
                process_file(os.path.join(dirpath, filename))

if __name__ == "__main__":
    main()
