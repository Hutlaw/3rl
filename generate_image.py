from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_random_image():
    # Image settings
    width, height = 800, 600  # 4:3 ratio
    background_color = (0, 0, 0)  # Black background
    text_color = (255, 255, 255)  # White text

    # Create a new image with black background
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Generate 3 random capitalized letters
    random_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))

    # Load a font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Default font path for Linux
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    # Add the random letters in the center of the image
    text_width, text_height = draw.textsize(random_letters, font=font)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), random_letters, font=font, fill=text_color)

    # Add the "@3randomletters.bsky.social" text in the bottom right corner
    handle_text = "@3randomletters.bsky.social"
    handle_text_size = 20
    handle_font = ImageFont.truetype(font_path, handle_text_size)
    handle_text_width, handle_text_height = draw.textsize(handle_text, font=handle_font)
    handle_x = width - handle_text_width - 10  # Padding from the edge
    handle_y = height - handle_text_height - 10
    draw.text((handle_x, handle_y), handle_text, font=handle_font, fill=text_color)

    # Save image as "random_image.png" and overwrite the previous one
    img.save('random_image.png')

if __name__ == "__main__":
    generate_random_image()
