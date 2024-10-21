from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_random_image():
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

    random_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))

    with open("random_letters.txt", "w") as file:
        file.write(random_letters)

    font_size = 100
    font_path = "Comic Sans MS.ttf"
    if not os.path.exists(font_path):
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, font_size)

    text_bbox = draw.textbbox((0, 0), random_letters, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    draw.text((text_x - shadow_offset, text_y - shadow_offset), random_letters, font=font, fill=outline_color)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), random_letters, font=font, fill=outline_color)
    
    draw.text((text_x, text_y), random_letters, font=font, fill=text_color)

    handle_text = "@3randomletters.bsky.social"
    handle_font = ImageFont.truetype(font_path, 20) if os.path.exists(font_path) else ImageFont.load_default()
    handle_bbox = draw.textbbox((0, 0), handle_text, font=handle_font)
    handle_text_width, handle_text_height = handle_bbox[2] - handle_bbox[0], handle_bbox[3] - handle_bbox[1]
    handle_x = width - handle_text_width - 20
    handle_y = height - handle_text_height - 20

    draw.text((handle_x - shadow_offset, handle_y - shadow_offset), handle_text, font=handle_font, fill=outline_color)
    draw.text((handle_x, handle_y), handle_text, font=handle_font, fill=text_color)

    img.save('random_image.png')
    return random_letters

if __name__ == "__main__":
    generate_random_image()
