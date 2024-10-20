from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def generate_random_image():
    width, height = 640, 480
    background_color_top = (50, 50, 50)  # Lightened the background
    background_color_bottom = (30, 30, 30)  # Gradient to a darker color
    text_color = (255, 255, 255)  # White for the text
    outline_color = (0, 0, 0)  # Black outline for the text
    shadow_offset = 5
    glow_radius = 10

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Draw gradient background
    for y in range(height):
        color = tuple(
            int(background_color_top[i] + (background_color_bottom[i] - background_color_top[i]) * y / height) for i in range(3)
        )
        draw.line([(0, y), (width, y)], fill=color)

    # Generate random letters for the main text
    random_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))

    font_size = 100
    font = ImageFont.load_default()  # Using default font, make sure font is available

    # Calculate text position (centered)
    text_bbox = draw.textbbox((0, 0), random_letters, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    # Draw shadow effect for the text
    draw.text((text_x - shadow_offset, text_y - shadow_offset), random_letters, font=font, fill=outline_color)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), random_letters, font=font, fill=outline_color)
    
    # Draw main text
    draw.text((text_x, text_y), random_letters, font=font, fill=text_color)

    # Apply glow filter
    img = img.filter(ImageFilter.GaussianBlur(radius=glow_radius))

    # Add handle text at the bottom-right corner
    handle_text = "@3randomletters.bsky.social"
    handle_font = ImageFont.load_default()
    handle_bbox = draw.textbbox((0, 0), handle_text, font=handle_font)
    handle_text_width, handle_text_height = handle_bbox[2] - handle_bbox[0], handle_bbox[3] - handle_bbox[1]
    handle_x = width - handle_text_width - 20
    handle_y = height - handle_text_height - 20

    # Draw handle shadow
    draw.text((handle_x - shadow_offset, handle_y - shadow_offset), handle_text, font=handle_font, fill=outline_color)
    
    # Draw handle text
    draw.text((handle_x, handle_y), handle_text, font=handle_font, fill=text_color)

    # Save the image
    img.save('random_image.png')

if __name__ == "__main__":
    generate_random_image()
