import os
import re
import json
import requests
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
SOURCE_URL = os.environ.get("SOURCE_URL")
CHANNEL_GROUPS_RAW = os.getenv("CHANNEL_GROUPS")

if not SOURCE_URL or not CHANNEL_GROUPS_RAW:
    print("❌ SOURCE_URL or CHANNEL_GROUPS not set in .env")
    exit()

# Parse CHANNEL_GROUPS from .env
try:
    channel_groups = json.loads(CHANNEL_GROUPS_RAW)
except json.JSONDecodeError as e:
    print(f"❌ Invalid CHANNEL_GROUPS format: {e}")
    exit()

# Map allowed channels to their group
allowed_channels = {}
for group, channels in channel_groups.items():
    for name in channels:
        allowed_channels[name.lower()] = group

# === Define your custom channel metadata ===
custom_channel_data = {
  "disney channel": {
    "tvg-id": "1373",
    "tvg-name": "Hello",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Disney_Channel.png",
    "display-name": "Disney Channel"
  },
  "disney junior": {
    "tvg-id": "1374",
    "tvg-name": "Disney Junior",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Disney_Junior.png",
    "display-name": "Disney Junior"
  },
  "hungama": {
    "tvg-id": "1391",
    "tvg-name": "Hungama",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Hungama.png",
    "display-name": "Hungama"
  },
  "super hungama": {
    "tvg-id": "1392",
    "tvg-name": "Super Hungama",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Super_Hungama.png",
    "display-name": "Super Hungama"
  },
  "star plus hd": {
    "tvg-id": "1132",
    "tvg-name": "Star Plus HD",
    "tvg-logo": "https://watchindia.net/images/channels/hindi/Star_Plus_HD.png",
    "display-name": "Star Plus HD"
  },
  "star plus": {
    "tvg-id": "1116",
    "tvg-name": "Star Plus",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Plus.png",
    "display-name": "Star Plus"
  },
  "star gold hd": {
    "tvg-id": "156",
    "tvg-name": "Star Gold HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Gold_HD.png",
    "display-name": "Star Gold HD"
  },
  "star gold 2": {
    "tvg-id": "1154",
    "tvg-name": "Star Gold 2",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Gold_2.png",
    "display-name": "Star Gold 2"
  },
  "star gold 2 hd": {
    "tvg-id": "1155",
    "tvg-name": "Star Gold 2 HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Gold_2_HD.png",
    "display-name": "Star Gold 2 HD"
  },
  "star bharat hd": {
    "tvg-id": "931",
    "tvg-name": "Star Bharat HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Bharat_HD.png",
    "display-name": "Star Bharat HD"
  },
  "star bharat": {
    "tvg-id": "1127",
    "tvg-name": "Star Bharat",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Bharat.png",
    "display-name": "Star Bharat"
  },
  "star gold": {
    "tvg-id": "1125",
    "tvg-name": "Star Gold",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Gold.png",
    "display-name": "Star Gold"
  },
  "star gold select hd": {
    "tvg-id": "1113",
    "tvg-name": "Star Gold Select HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Gold_Select_HD.png",
    "display-name": "Star Gold Select HD"
  },
  "star sports 1 hindi hd": {
    "tvg-id": "173",
    "tvg-name": "Star Sports 1 Hindi HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Sports_HD1_Hindi.png",
    "display-name": "Star Sports 1 Hindi HD"
  },
  "star sports select 1 hd": {
    "tvg-id": "300",
    "tvg-name": "Star Sports Select 1 HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Sports_Select_HD_1.png",
    "display-name": "Star Sports Select 1 HD"
  },
  "star sports select 2 hd": {
    "tvg-id": "301",
    "tvg-name": "Star Sports Select 2 HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Sports_Select_HD_2.png",
    "display-name": "Star Sports Select 2 HD"
  },
  "star gold select": {
    "tvg-id": "1119",
    "tvg-name": "Star Gold Select",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Star_Gold_Select.png",
    "display-name": "Star Gold Select"
  },
  "colors hd": {
    "tvg-id": "144",
    "tvg-name": "Colors HD",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Colors_HD.png",
    "display-name": "Colors HD"
  },
  "abp news india": {
    "tvg-id": "177",
    "tvg-name": "ABP News India",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/ABP_News_India.png",
    "display-name": "ABP News India"
  },
  "dd news": {
    "tvg-id": "203",
    "tvg-name": "DD News",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/DD_News.png",
    "display-name": "DD News"
  },
  "news 18 india": {
    "tvg-id": "231",
    "tvg-name": "News 18 India",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/IBN_7.png",
    "display-name": "News 18 India"
  },
  "india tv": {
    "tvg-id": "235",
    "tvg-name": "India TV",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/India_TV.png",
    "display-name": "India TV"
  },
  "ndtv india": {
    "tvg-id": "258",
    "tvg-name": "NDTV India",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/NDTV_India.png",
    "display-name": "NDTV India"
  },
  "colors cineplex": {
    "tvg-id": "482",
    "tvg-name": "Colors Cineplex",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Colors_Cineplex.png",
    "display-name": "Colors Cineplex"
  },
  "india news": {
    "tvg-id": "498",
    "tvg-name": "India news",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/India_news.png",
    "display-name": "India news"
  },
  "nick hindi": {
    "tvg-id": "545",
    "tvg-name": "Nick Hindi",
    "tvg-logo": "https://jiotvimages.cdn.jio.com/dare_images/images/Nick_Hindi.png",
    "display-name": "Nick Hindi"
  }

    # Add more channel customizations here
}

# === Fetch playlist ===
print(f"📥 Fetching playlist from: {SOURCE_URL}")
try:
    response = requests.get(SOURCE_URL)
    response.raise_for_status()
    lines = response.text.splitlines()
except Exception as e:
    print(f"❌ Error fetching playlist: {e}")
    exit()

# === Process playlist blocks ===
full_blocks = []
i = 0
while i < len(lines) - 5:
    if lines[i].startswith("#EXTINF:") and \
       lines[i+1].startswith("#KODIPROP:") and \
       lines[i+2].startswith("#KODIPROP:") and \
       lines[i+3].startswith("#EXTVLCOPT:") and \
       lines[i+4].startswith("#EXTHTTP:") and \
       lines[i+5].startswith("https"):

        extinf = lines[i]
        try:
            channel_name = extinf.split(",")[-1].strip()
            group = allowed_channels.get(channel_name.lower())
        except:
            group = None

        if group:
            # Use your custom EXTINF if available
            channel_key = channel_name.lower()
            custom_info = custom_channel_data.get(channel_key)

            if custom_info:
                updated_extinf = (
                    f'#EXTINF:-1 tvg-id="{custom_info.get("tvg-id", "")}" '
                    f'tvg-name="{custom_info.get("tvg-name", "")}" '
                    f'group-title="{group}" '
                    f'tvg-logo="{custom_info.get("tvg-logo", "")}",' 
                    f'{custom_info.get("display-name", channel_name)}'
                )
            else:
                # fallback: only update group-title
                updated_extinf = re.sub(r'group-title=".*?"', f'group-title="{group}"', extinf)

            block = "\n".join([
                updated_extinf,
                lines[i+1],
                lines[i+2],
                lines[i+3],
                lines[i+4],
                lines[i+5]
            ])
            full_blocks.append(block)
            i += 6
            continue
    i += 1

# === Write output file ===
output_file = "jiotv.m3u"
if os.path.exists(output_file):
    os.remove(output_file)

with open(output_file, "w", encoding="utf-8") as f:
    if full_blocks:
        print(f"✅ Found {len(full_blocks)} categorized channels.")
        f.write("#EXTM3U\n# Updated By Himanshu\n\n")
        for block in full_blocks:
            f.write(block + "\n")
    else:
        print("⚠️ No matching channels found.")
        f.write("#EXTM3U\n# No matching channels found\n")

os.chmod(output_file, 0o666)
print(f"✅ '{output_file}' written with category assignments.")
