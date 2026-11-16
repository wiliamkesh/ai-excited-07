import random
from PIL import Image, ImageDraw, ImageFilter
import os

def generate_image():
    # Set seed for determinism
    random.seed(42)
    
    width, height = 1024, 1024
    # Deep indigo/violet background for the "night" and general space
    bg_color = (10, 5, 30)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 1. Draw the "Night" inside the crack first (as a base layer)
    # Deep violet nebula effect
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(50, 300)
        color = (random.randint(20, 60), random.randint(10, 40), random.randint(60, 120))
        # Draw a soft blob
        soft_blob = Image.new("RGBA", (radius*2, radius*2), (0,0,0,0))
        blob_draw = ImageDraw.Draw(soft_blob)
        for r in range(radius, 0, -5):
            alpha = int(20 * (1 - r/radius))
            blob_draw.ellipse([radius-r, radius-r, radius+r, radius+r], fill=(color[0], color[1], color[2], alpha))
        img.paste(soft_blob, (x-radius, y-radius), soft_blob)

    # 2. Draw the colossal orange sun
    sun_center = (width // 2, height // 2 - 50)
    sun_radius = 420
    
    # Sun glow
    for r in range(sun_radius + 60, sun_radius, -2):
        alpha = int(100 * (1 - (r - sun_radius) / 60))
        draw.ellipse([sun_center[0]-r, sun_center[1]-r, sun_center[0]+r, sun_center[1]+r], 
                     outline=(255, 140, 0, alpha))

    # Sun surface (textured orange/amber)
    for r in range(sun_radius, 0, -2):
        # Gradient from bright rim to deeper orange
        ratio = r / sun_radius
        color = (255, int(120 + 80 * ratio), int(20 + 40 * ratio))
        draw.ellipse([sun_center[0]-r, sun_center[1]-r, sun_center[0]+r, sun_center[1]+r], fill=color)

    # Add some "texture" to sun
    for _ in range(1000):
        angle = random.uniform(0, 2 * 3.14159)
        dist = random.uniform(0, sun_radius)
        x = int(sun_center[0] + dist * (random.random() * 0.5 + 0.5) * (1.0 if random.random() > 0.5 else -1.0)) # simplified jitter
        # better random point in circle
        dist = sun_radius * (random.random()**0.5)
        x = int(sun_center[0] + dist * random.uniform(-1, 1))
        y = int(sun_center[1] + dist * random.uniform(-1, 1))
        if ((x-sun_center[0])**2 + (y-sun_center[1])**2) < sun_radius**2:
            draw.point((x, y), fill=(255, 180, 50))

    # 3. CRACK OPEN down the middle (The Fissure)
    # The crack is a vertical fissure with glowing torn edges
    crack_width = 120
    crack_points = []
    for y in range(sun_center[1] - sun_radius, sun_center[1] + sun_radius + 1, 10):
        jitter = random.randint(-15, 15)
        crack_points.append((sun_center[0] + jitter, y))
    
    # Fill the crack with the "Night" (it already has nebula, but let's make it distinct)
    # We'll use a polygon to "cut" the sun
    crack_poly_left = [(sun_center[0] - crack_width//2 + random.randint(-10, 10), y) for _, y in crack_points]
    crack_poly_right = [(sun_center[0] + crack_width//2 + random.randint(-10, 10), y) for _, y in reversed(crack_points)]
    crack_poly = crack_poly_left + crack_poly_right
    
    draw.polygon(crack_poly, fill=(15, 5, 40)) # Dark interior
    
    # Inside the fissure: stars and a crescent moon
    for _ in range(50):
        x = random.randint(sun_center[0] - crack_width//2, sun_center[0] + crack_width//2)
        y = random.randint(sun_center[1] - sun_radius, sun_center[1] + sun_radius)
        # Check if inside crack (simplified)
        if abs(x - sun_center[0]) < crack_width // 2:
             draw.point((x, y), fill=(255, 255, 255))

    # Crescent moon inside crack
    moon_pos = (sun_center[0], sun_center[1] - 150)
    draw.ellipse([moon_pos[0]-20, moon_pos[1]-20, moon_pos[0]+20, moon_pos[1]+20], fill=(200, 200, 255))
    draw.ellipse([moon_pos[0]-10, moon_pos[1]-20, moon_pos[0]+30, moon_pos[1]+20], fill=(15, 5, 40))

    # ENORMOUS glowing golden eye
    eye_pos = (sun_center[0], sun_center[1] + 50)
    draw.ellipse([eye_pos[0]-40, eye_pos[1]-25, eye_pos[0]+40, eye_pos[1]+25], fill=(255, 215, 0)) # Sclera
    draw.ellipse([eye_pos[0]-15, eye_pos[1]-15, eye_pos[0]+15, eye_pos[1]+15], fill=(0, 0, 0)) # Pupil
    # Eye glow
    eye_glow = Image.new("RGBA", (width, height), (0,0,0,0))
    eg_draw = ImageDraw.Draw(eye_glow)
    for r in range(60, 40, -2):
        alpha = int(150 * (1 - (r-40)/20))
        eg_draw.ellipse([eye_pos[0]-r, eye_pos[1]-r, eye_pos[0]+r, eye_pos[1]+r], fill=(255, 255, 0, alpha))
    img.paste(eye_glow, (0,0), eye_glow)

    # Torn edges of the crack (glowing)
    for p in crack_poly_left + crack_poly_right:
        draw.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=(255, 255, 200))

    # 4. Dark rocky cliff at the bottom
    cliff_y = 850
    draw.rectangle([0, cliff_y, width, height], fill=(10, 10, 15))
    # Jagged top
    cliff_points = [(0, cliff_y)]
    for x in range(0, width + 1, 40):
        cliff_points.append((x, cliff_y + random.randint(-20, 20)))
    cliff_points.extend([(width, height), (0, height)])
    draw.polygon(cliff_points, fill=(5, 5, 10))

    # 5. Tiny Robot Silhouette
    robot_x = 400
    robot_y = 830
    # Body
    draw.rectangle([robot_x-5, robot_y-15, robot_x+5, robot_y], fill=(20, 20, 30))
    # Head
    draw.ellipse([robot_x-6, robot_y-25, robot_x+6, robot_y-15], fill=(20, 20, 30))
    # Teal rim light on robot
    draw.line([robot_x+6, robot_y-25, robot_x+6, robot_y], fill=(0, 255, 255), width=1)
    # Arms reacting
    draw.line([robot_x-5, robot_y-12, robot_x-15, robot_y-25], fill=(20, 20, 30), width=2) # arm shielding face
    draw.line([robot_x+5, robot_y-12, robot_x+20, robot_y-30], fill=(20, 20, 30), width=2) # arm raised toward light

    # 6. Debris and particles streaming
    for _ in range(300):
        # Start from bottom/cliff area
        start_x = random.randint(0, width)
        start_y = random.randint(cliff_y - 100, height)
        # Pull toward the crack
        target_x = sun_center[0] + random.randint(-crack_width//2, crack_width//2)
        target_y = sun_center[1] + random.randint(-sun_radius, sun_radius)
        
        # Draw a streak
        length = random.uniform(0.1, 0.4)
        end_x = start_x + (target_x - start_x) * length
        end_y = start_y + (target_y - start_y) * length
        
        color = (random.randint(200, 255), random.randint(150, 200), random.randint(50, 100))
        draw.line([start_x, start_y, end_x, end_y], fill=color, width=random.randint(1, 2))

    # Final polish: overall glow
    img = img.filter(ImageFilter.SMOOTH_MORE)

    # Create output directory
    os.makedirs("out", exist_ok=True)
    
    # Save the image
    img.save("out/entry.png", "PNG", optimize=True)
    print(f"Image saved to out/entry.png. Size: {os.path.getsize('out/entry.png')} bytes")

if __name__ == "__main__":
    generate_image()
