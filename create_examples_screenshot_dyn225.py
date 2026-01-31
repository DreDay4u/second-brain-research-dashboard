#!/usr/bin/env python3
"""
Create screenshot showing variety enforcement examples.

Visual representation of valid vs invalid component configurations.
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('screenshots', exist_ok=True)

WIDTH = 1400
HEIGHT = 1600
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (30, 30, 30)
SUCCESS_COLOR = (34, 197, 94)
FAIL_COLOR = (239, 68, 68)
HEADER_BG = (59, 130, 246)
BORDER_COLOR = (229, 231, 235)
COMPONENT_BG = (243, 244, 246)

img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    mono_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
except:
    title_font = header_font = body_font = small_font = mono_font = ImageFont.load_default()

# Header
draw.rectangle([(0, 0), (WIDTH, 80)], fill=HEADER_BG)
draw.text((50, 25), "Variety Enforcement Examples", fill=(255, 255, 255), font=title_font)

y_pos = 120

# Example 1: VALID
draw.rectangle([(50, y_pos-10), (WIDTH-50, y_pos+30)], fill=SUCCESS_COLOR)
draw.text((60, y_pos), "✅ VALID Example: Good Variety (4 types, no 3+ consecutive)", fill=(255, 255, 255), font=header_font)
y_pos += 50

components_valid = [
    ("a2ui.TLDR", "tldr-1", None),
    ("a2ui.StatCard", "stat-1", None),
    ("a2ui.HeadlineCard", "headline-1", None),
    ("a2ui.VideoCard", "video-1", None),
    ("a2ui.StatCard", "stat-2", None),
]

for i, (comp_type, comp_id, marker) in enumerate(components_valid):
    comp_y = y_pos + i * 45
    draw.rectangle([(70, comp_y), (WIDTH-70, comp_y+35)], outline=BORDER_COLOR, width=1, fill=COMPONENT_BG)
    draw.text((90, comp_y+8), f"{i+1}. {comp_type}", fill=TEXT_COLOR, font=mono_font)
    draw.text((WIDTH-200, comp_y+8), f"id: {comp_id}", fill=(107, 114, 128), font=small_font)

y_pos += len(components_valid) * 45 + 20
draw.text((70, y_pos), "✓ 4 unique types  ✓ Max 2 consecutive", fill=SUCCESS_COLOR, font=body_font)

y_pos += 60

# Example 2: VALID with 2 consecutive
draw.rectangle([(50, y_pos-10), (WIDTH-50, y_pos+30)], fill=SUCCESS_COLOR)
draw.text((60, y_pos), "✅ VALID: 2 Consecutive Allowed", fill=(255, 255, 255), font=header_font)
y_pos += 50

components_valid2 = [
    ("a2ui.TLDR", "tldr-1", None),
    ("a2ui.StatCard", "stat-1", "← 1st"),
    ("a2ui.StatCard", "stat-2", "← 2nd consecutive (OK)"),
    ("a2ui.HeadlineCard", "headline-1", None),
    ("a2ui.VideoCard", "video-1", None),
]

for i, (comp_type, comp_id, marker) in enumerate(components_valid2):
    comp_y = y_pos + i * 45
    draw.rectangle([(70, comp_y), (WIDTH-70, comp_y+35)], outline=BORDER_COLOR, width=1, fill=COMPONENT_BG)
    draw.text((90, comp_y+8), f"{i+1}. {comp_type}", fill=TEXT_COLOR, font=mono_font)
    if marker:
        draw.text((WIDTH-350, comp_y+8), marker, fill=SUCCESS_COLOR, font=small_font)

y_pos += len(components_valid2) * 45 + 20
draw.text((70, y_pos), "✓ 4 unique types  ✓ Exactly 2 consecutive", fill=SUCCESS_COLOR, font=body_font)

y_pos += 60

# Example 3: INVALID - insufficient types
draw.rectangle([(50, y_pos-10), (WIDTH-50, y_pos+30)], fill=FAIL_COLOR)
draw.text((60, y_pos), "❌ INVALID: Only 2 Unique Types (Need 4+)", fill=(255, 255, 255), font=header_font)
y_pos += 50

components_invalid1 = [
    ("a2ui.StatCard", "s1", None),
    ("a2ui.StatCard", "s2", None),
    ("a2ui.HeadlineCard", "h1", None),
    ("a2ui.StatCard", "s3", None),
]

for i, (comp_type, comp_id, marker) in enumerate(components_invalid1):
    comp_y = y_pos + i * 45
    bg_color = (254, 226, 226) if comp_type == "a2ui.StatCard" else COMPONENT_BG
    draw.rectangle([(70, comp_y), (WIDTH-70, comp_y+35)], outline=BORDER_COLOR, width=1, fill=bg_color)
    draw.text((90, comp_y+8), f"{i+1}. {comp_type}", fill=TEXT_COLOR, font=mono_font)

y_pos += len(components_invalid1) * 45 + 20
draw.text((70, y_pos), "✗ Only 2 unique types (need 4+)", fill=FAIL_COLOR, font=body_font)

y_pos += 60

# Example 4: INVALID - too many consecutive
draw.rectangle([(50, y_pos-10), (WIDTH-50, y_pos+30)], fill=FAIL_COLOR)
draw.text((60, y_pos), "❌ INVALID: 3 Consecutive Same Type", fill=(255, 255, 255), font=header_font)
y_pos += 50

components_invalid2 = [
    ("a2ui.TLDR", "tldr-1", None),
    ("a2ui.StatCard", "s1", "← 1st"),
    ("a2ui.StatCard", "s2", "← 2nd"),
    ("a2ui.StatCard", "s3", "← 3rd VIOLATION!"),
    ("a2ui.HeadlineCard", "h1", None),
    ("a2ui.VideoCard", "v1", None),
]

for i, (comp_type, comp_id, marker) in enumerate(components_invalid2):
    comp_y = y_pos + i * 45
    is_violation = i >= 1 and i <= 3
    bg_color = (254, 226, 226) if is_violation else COMPONENT_BG
    draw.rectangle([(70, comp_y), (WIDTH-70, comp_y+35)], outline=BORDER_COLOR, width=2 if i == 3 else 1, fill=bg_color)
    draw.text((90, comp_y+8), f"{i+1}. {comp_type}", fill=TEXT_COLOR, font=mono_font)
    if marker:
        color = FAIL_COLOR if "VIOLATION" in marker else (107, 114, 128)
        draw.text((WIDTH-350, comp_y+8), marker, fill=color, font=small_font)

y_pos += len(components_invalid2) * 45 + 20
draw.text((70, y_pos), "✗ Found 3 consecutive StatCard (max allowed: 2)", fill=FAIL_COLOR, font=body_font)

# Footer
y_pos = HEIGHT - 80
draw.text((50, y_pos), "Variety Enforcement Rules:", fill=TEXT_COLOR, font=body_font)
y_pos += 25
draw.text((70, y_pos), "1. Minimum 4 unique component types per dashboard", fill=(107, 114, 128), font=small_font)
y_pos += 20
draw.text((70, y_pos), "2. No more than 2 consecutive components of same type", fill=(107, 114, 128), font=small_font)

output_path = 'screenshots/DYN-225-variety-examples.png'
img.save(output_path)
print(f"✅ Examples screenshot saved to: {output_path}")
print(f"   Dimensions: {WIDTH}x{HEIGHT}")
print(f"   Examples: 2 valid, 2 invalid")
