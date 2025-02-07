from PIL import Image, ImageDraw, ImageFont
import json
import os

with open("manual/config.json", "r") as file:
    config = json.load(file)

def generate_image(letter_count, letters):
    if not letters:
        print(f"Skipping {letter_count}-letter image: No letters defined.")
        return

    width, height = 640, 480
    background_color_top = (50, 50, 50)
    background_color_bottom = (30, 30, 30)
    text_color = (255, 255, 255)
    outline_color = (0, 0, 0)
    shadow_offset = 5

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        color = tuple(
            int(background_color_top[i] + (background_color_bottom[i] - background_color_top[i]) * y / height) for i in range(3)
        )
        draw.line([(0, y), (width, y)], fill=color)

    font_size = 100
    font_path = "Short Baby.ttf"
    font = ImageFont.truetype(font_path, font_size) if os.path.exists(font_path) else ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), letters, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    draw.text((text_x - shadow_offset, text_y - shadow_offset), letters, font=font, fill=outline_color)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), letters, font=font, fill=outline_color)
    draw.text((text_x, text_y), letters, font=font, fill=text_color)

    handle_text = f'@{letter_count}randomletters.bsky.social'
    handle_font = ImageFont.truetype(font_path, 20) if os.path.exists(font_path) else ImageFont.load_default()
    handle_bbox = draw.textbbox((0, 0), handle_text, font=handle_font)
    handle_text_width, handle_text_height = handle_bbox[2] - handle_bbox[0], handle_bbox[3] - handle_bbox[1]
    handle_x = width - handle_text_width - 20
    handle_y = height - handle_text_height - 20

    draw.text((handle_x - shadow_offset, handle_y - shadow_offset), handle_text, font=handle_font, fill=outline_color)
    draw.text((handle_x, handle_y), handle_text, font=handle_font, fill=text_color)

    img.save(f'manual/random_image_{letter_count}.png')

    with open(f'manual/random_letters_{letter_count}.txt', "w") as file:
        file.write(letters)

for count in [3, 4, 5]:
    generate_image(count, config[f"{count}_letter"])
