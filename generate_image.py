from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_random_image():
    width, height = 800, 600
    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    random_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    text_width, text_height = font.getsize(random_letters)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), random_letters, font=font, fill=text_color)

    handle_text = "@3randomletters.bsky.social"
    handle_text_size = 20
    handle_font = ImageFont.truetype(font_path, handle_text_size)
    handle_text_width, handle_text_height = handle_font.getsize(handle_text)
    handle_x = width - handle_text_width - 10
    handle_y = height - handle_text_height - 10
    draw.text((handle_x, handle_y), handle_text, font=handle_font, fill=text_color)

    img.save('random_image.png')

if __name__ == "__main__":
    generate_random_image()
