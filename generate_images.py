#!/usr/bin/env python3
"""
Generate featured tweet images for The AI Enterprise Report.
Usage: python generate_images.py "<alexwg_title>" "<company_name>" "<ethan_topic>" [date_str]

Arguments:
  alexwg_title  - Short title for @alexwg's daily theme (e.g., "AI AGENTS SURGE")
  company_name  - Enterprise company name (e.g., "ServiceNow")
  ethan_topic   - Short topic for Ethan's take (e.g., "VENDOR LOCK-IN")
  date_str      - Optional date string for filenames (default: today YYYY-MM-DD)

Outputs images to ./images/ directory:
  images/alexwg-{date}.png
  images/{company}-{date}.png
  images/ethan-{date}.png
"""

import sys, os, math
from PIL import Image, ImageDraw, ImageFont
from datetime import date

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)
W, H = 800, 400

def get_font(size):
    paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/Library/Fonts/Arial Bold.ttf",
             "/System/Library/Fonts/Helvetica.ttc",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

def draw_gradient(img, color1, color2):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(color1[0] + (color2[0] - color1[0]) * y / H)
        g = int(color1[1] + (color2[1] - color1[1]) * y / H)
        b = int(color1[2] + (color2[2] - color1[2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return draw

# Company color schemes
COMPANY_THEMES = {
    "salesforce":    {"colors": ((0,40,80),(0,90,170)),  "accent": (0,176,240),   "handle": "@salesforce"},
    "servicenow":    {"colors": ((20,50,20),(40,100,40)), "accent": (129,199,132), "handle": "@ServiceNow"},
    "microsoft":     {"colors": ((20,20,50),(50,50,120)), "accent": (0,120,215),   "handle": "@Microsoft"},
    "sap":           {"colors": ((30,30,60),(60,60,120)), "accent": (0,143,211),   "handle": "@SAP"},
    "oracle":        {"colors": ((60,10,10),(120,20,20)), "accent": (255,0,0),     "handle": "@Oracle"},
    "workday":       {"colors": ((50,30,10),(100,60,20)), "accent": (255,123,0),   "handle": "@Workday"},
    "snowflake":     {"colors": ((10,30,50),(30,80,130)), "accent": (41,171,226),  "handle": "@SnowflakeDB"},
    "databricks":    {"colors": ((50,10,10),(100,30,30)), "accent": (255,59,48),   "handle": "@datababoricks"},
    "palantir":      {"colors": ((10,10,10),(40,40,40)),  "accent": (255,255,255), "handle": "@PalantirTech"},
    "ibm":           {"colors": ((0,20,50),(0,50,100)),   "accent": (0,98,152),    "handle": "@IBM"},
    "google cloud":  {"colors": ((15,35,60),(30,70,120)), "accent": (66,133,244),  "handle": "@googlecloud"},
    "aws":           {"colors": ((20,20,30),(40,40,60)),  "accent": (255,153,0),   "handle": "@awscloud"},
    "datadog":       {"colors": ((40,20,50),(80,40,100)), "accent": (99,44,166),   "handle": "@databoradoghq"},
    "crowdstrike":   {"colors": ((50,10,10),(100,20,20)), "accent": (255,52,52),   "handle": "@CrowdStrike"},
    "atlassian":     {"colors": ((10,20,50),(20,50,110)), "accent": (0,82,204),    "handle": "@Atlassian"},
    "hubspot":       {"colors": ((50,20,10),(100,40,20)), "accent": (255,122,89),  "handle": "@HubSpot"},
    "mongodb":       {"colors": ((10,30,10),(30,70,30)),  "accent": (71,162,72),   "handle": "@MongoDB"},
    "elastic":       {"colors": ((10,40,40),(20,80,70)),  "accent": (0,191,179),   "handle": "@elastic"},
}

def generate_alexwg(title, date_str):
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, (10, 15, 40), (25, 50, 100))
    # Grid with glowing nodes
    for i in range(0, W, 60):
        draw.line([(i, 0), (i, H)], fill=(40, 70, 140), width=1)
    for i in range(0, H, 60):
        draw.line([(0, i), (W, i)], fill=(40, 70, 140), width=1)
    for x in range(30, W, 120):
        for y in range(30, H, 120):
            for r in range(12, 0, -1):
                draw.ellipse([x-r, y-r, x+r, y+r], fill=(29+r*5, 80+r*8, 180+r*5))
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(100, 180, 255))
            if x + 120 < W:
                draw.line([(x, y), (x+120, y)], fill=(50, 100, 180), width=1)
            if y + 120 < H:
                draw.line([(x, y), (x, y+120)], fill=(50, 100, 180), width=1)
    # Text
    draw.text((W//2, H//2-40), "THE INNERMOST LOOP", fill=(255,255,255), font=get_font(36), anchor="mm")
    draw.text((W//2, H//2+10), "Dr. Alex Wissner-Gross", fill=(150,200,255), font=get_font(18), anchor="mm")
    draw.text((W//2, H//2+40), title.upper(), fill=(120,160,220), font=get_font(14), anchor="mm")
    draw.rectangle([0,0,W,4], fill=(29,155,240))
    path = f"{OUT}/alexwg-{date_str}.png"
    img.save(path, quality=90)
    return f"images/alexwg-{date_str}.png"

def generate_company(company_name, date_str):
    key = company_name.lower()
    theme = COMPANY_THEMES.get(key, {"colors": ((20,20,50),(50,50,120)), "accent": (100,150,255), "handle": f"@{company_name}"})
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, theme["colors"][0], theme["colors"][1])
    # Wave pattern
    for wave in range(3):
        y_base = 100 + wave * 100
        points = [(x, y_base + math.sin(x/60+wave*2)*30 + math.cos(x/40)*15) for x in range(0, W+1, 4)]
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=(*theme["accent"][:3],), width=2)
    # Agent nodes
    positions = [(150,120),(350,80),(550,140),(250,250),(450,280),(650,200)]
    for i,(ax,ay) in enumerate(positions):
        for r in range(20,0,-1):
            c = int(200*r/20)
            draw.ellipse([ax-r,ay-r,ax+r,ay+r], fill=(c,c+30,255))
        draw.ellipse([ax-8,ay-8,ax+8,ay+8], fill=(255,255,255))
        for j,(bx,by) in enumerate(positions):
            if j>i and abs(ax-bx)<250:
                draw.line([(ax,ay),(bx,by)], fill=(*theme["accent"][:3],), width=1)
    draw.text((W//2, H//2+50), company_name.upper(), fill=(255,255,255), font=get_font(32), anchor="mm")
    draw.text((W//2, H//2+85), f"{company_name} AI", fill=(180,220,255), font=get_font(20), anchor="mm")
    draw.rectangle([0,0,W,4], fill=theme["accent"])
    slug = company_name.lower().replace(" ", "-")
    path = f"{OUT}/{slug}-{date_str}.png"
    img.save(path, quality=90)
    return f"images/{slug}-{date_str}.png"

def generate_ethan(topic, date_str):
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, (30,10,10), (80,20,20))
    # Corrupted data visual
    for y in range(0, H, 8):
        x_offset = int(math.sin(y/20)*15) if H//3 < y < 2*H//3 else 0
        brightness = 40 + int(20*math.sin(y/30))
        draw.line([(x_offset,y),(W+x_offset,y)], fill=(brightness,brightness//2,brightness//2), width=1)
    for col in range(0, W, 80):
        for row in range(0, H, 40):
            if (col+row) % 160 < 80:
                draw.rectangle([col+2,row+2,col+76,row+36], outline=(60,100,60), width=1)
            else:
                shift = int(math.sin((col+row)/50)*8)
                draw.rectangle([col+2+shift,row+2,col+76+shift,row+36], outline=(150,40,40), width=1)
                for g in range(3):
                    gy = row+8+g*10
                    draw.line([(col+shift+5,gy),(col+shift+50+g*8,gy)], fill=(200,50,50), width=2)
    draw.rectangle([W//2-200,H//2-50,W//2+200,H//2+50], fill=(20,5,5))
    draw.text((W//2,H//2-15), topic.upper(), fill=(255,80,80), font=get_font(36), anchor="mm")
    draw.text((W//2,H//2+25), "@ethanhill", fill=(255,120,120), font=get_font(18), anchor="mm")
    draw.rectangle([0,0,W,4], fill=(239,68,68))
    path = f"{OUT}/ethan-{date_str}.png"
    img.save(path, quality=90)
    return f"images/ethan-{date_str}.png"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    alexwg_title = sys.argv[1]
    company_name = sys.argv[2]
    ethan_topic = sys.argv[3]
    date_str = sys.argv[4] if len(sys.argv) > 4 else date.today().isoformat()

    p1 = generate_alexwg(alexwg_title, date_str)
    print(f"Created: {p1}")
    p2 = generate_company(company_name, date_str)
    print(f"Created: {p2}")
    p3 = generate_ethan(ethan_topic, date_str)
    print(f"Created: {p3}")
    print(f"\nImage paths for stories.json:")
    print(f'  alexwg: "{p1}"')
    print(f'  company: "{p2}"')
    print(f'  ethan: "{p3}"')
