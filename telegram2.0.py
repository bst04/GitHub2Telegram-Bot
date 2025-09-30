import requests
import random
from PIL import Image, ImageDraw, ImageFont
import io

# 🔑 Replace with your Telegram Bot token and chat_id
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
CHAT_ID = "TELEGRAM_ID"   # Can be a group ID or personal ID

# --- Get a random cybersecurity repo from GitHub ---
def get_cybersecurity_repo():
    url = "https://api.github.com/search/repositories"
    params = {"q": "cybersecurity", "sort": "stars", "order": "desc", "per_page": 50}
    response = requests.get(url, params=params)
    data = response.json()
    
    repo = random.choice(data["items"])
    return {
        "name": repo["name"],
        "desc": repo["description"],
        "url": repo["html_url"],
        "owner": repo["owner"]["login"],
        "avatar_url": repo["owner"]["avatar_url"]
    }

# --- Generate banner image with dynamic gradient ---
def generate_image(repo, filename="repo_post.png"):
    width, height = 1200, 600
    img = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    # Dynamic gradient colors
    start_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    end_color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y / height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y / height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # --- Load and paste avatar ---
    avatar_resp = requests.get(repo["avatar_url"])
    avatar = Image.open(io.BytesIO(avatar_resp.content)).convert("RGBA").resize((180, 180))
    mask = Image.new("L", avatar.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
    img.paste(avatar, (70, height//2 - 90), mask)

    # --- Fonts ---
    try:
        font_title = ImageFont.truetype("Arial Bold.ttf", 70)
        font_desc = ImageFont.truetype("Arial.ttf", 36)
        font_signature = ImageFont.truetype("Arial Italic.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_signature = ImageFont.load_default()

    # --- Repo title ---
    title_x, title_y = 300, 120
    draw.text((title_x, title_y), repo["name"], font=font_title, fill=(255, 255, 255))

    # --- Wrap description with right margin ---
    desc = repo["desc"] if repo["desc"] else "No description available."
    margin_right = 50
    text_area_width = width - title_x - margin_right

    words = desc.split()
    lines, line = [], ""
    for word in words:
        test_line = line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font_desc)
        test_width = bbox[2] - bbox[0]
        if test_width <= text_area_width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y_text = 230
    for line in lines[:5]:  # limit to 5 lines
        draw.text((title_x, y_text), line.strip(), font=font_desc, fill=(230, 230, 230))
        y_text += 45

    # --- Watermark signature ---
    signature = "cybst04"
    bbox = draw.textbbox((0, 0), signature, font=font_signature)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(
        (width - text_w - 30, height - text_h - 20),
        signature,
        font=font_signature,
        fill=(180, 180, 180)
    )

    img.save(filename)
    return filename

# --- Send message + image to Telegram ---
def send_to_telegram(message, image_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": message}, files={"photo": img})

# --- Main function ---
def run():
    repo = get_cybersecurity_repo()
    image_path = generate_image(repo)

    post_text = f"""
🚀 {repo['name']}

📝 {repo['desc']}

🔗 {repo['url']}
"""

    send_to_telegram(post_text, image_path)

if __name__ == "__main__":
    run()
