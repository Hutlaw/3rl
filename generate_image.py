import os
import sys
import random
from PIL import Image, ImageDraw, ImageFont

def generate_image(letter_count, letters=None):
    width, height = 640, 480
    background_top, background_bottom = (50, 50, 50), (30, 30, 30)
    text_color, outline_color, shadow_offset = (255, 255, 255), (0, 0, 0), 5

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        color = tuple(
            int(background_top[i] + (background_bottom[i] - background_top[i]) * y / height) for i in range(3)
        )
        draw.line([(0, y), (width, y)], fill=color)

    letters = letters or ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=letter_count))
    txt_file = f'random_letters_{letter_count}.txt'
    with open(txt_file, "w") as file:
        file.write(letters)

    font_path = "Short Baby.ttf"
    font = ImageFont.truetype(font_path, 100) if os.path.exists(font_path) else ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), letters, font=font)
    text_x = (width - (text_bbox[2] - text_bbox[0])) / 2
    text_y = (height - (text_bbox[3] - text_bbox[1])) / 2

    draw.text((text_x - shadow_offset, text_y - shadow_offset), letters, font=font, fill=outline_color)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), letters, font=font, fill=outline_color)
    draw.text((text_x, text_y), letters, font=font, fill=text_color)

    handle_text = f'@{letter_count}randomletters.bsky.social'
    handle_font = ImageFont.truetype(font_path, 20) if os.path.exists(font_path) else ImageFont.load_default()
    handle_bbox = draw.textbbox((0, 0), handle_text, font=handle_font)
    handle_x = width - (handle_bbox[2] - handle_bbox[0]) - 20
    handle_y = height - (handle_bbox[3] - handle_bbox[1]) - 20

    draw.text((handle_x - shadow_offset, handle_y - shadow_offset), handle_text, font=handle_font, fill=outline_color)
    draw.text((handle_x, handle_y), handle_text, font=handle_font, fill=text_color)

    img.save(f'random_image_{letter_count}.png')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "manual":
        print("Custom letter input mode activated.")
        while True:
            account = input("Select Bluesky account (3, 4, 5) or cancel: ")
            if account.lower() == "cancel":
                print("Cancelled.")
                exit()
            if account not in ["3", "4", "5"]:
                print("Invalid account selection. Try again.")
                continue
            
            letter_count = int(account)
            letters = input(f"Enter {letter_count} custom letters: ").upper()
            if len(letters) != letter_count:
                print(f"Incorrect length! Must be exactly {letter_count} letters.")
                continue
            
            generate_image(letter_count, letters)
            if input("Push only this image? (yes/no): ").lower() == "yes":
                exit()

    for letter_count in [3, 4, 5]:
        generate_image(letter_count)