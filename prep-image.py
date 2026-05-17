# take image as input and convert to 1920px width jpg. output to ./public by default
# usage: python prep-image.py input.jpg output.jpg
# input can be a file path or URL (including Google Photos links)
import sys
import re
from PIL import Image
from io import BytesIO
from pathlib import Path
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    from urllib.request import urlopen, Request
    from urllib.error import URLError
def prep_image(input_path, output_path):
    with Image.open(input_path) as img:
        # Scale the image to fit within 1920px width while maintaining aspect ratio
        max_width = 1920
        max_height = img.size[1] * (1920 / img.size[0])  # Calculate proportional height
        img.thumbnail((max_width, max_height), Image.Resampling.BICUBIC)
        # Save as jpg
        img.save(output_path, 'JPEG', quality=85)

def extract_image_url_from_google_photos(html_content):
    """Extract image URL from Google Photos HTML page"""
    # Find all potential image URLs
    image_urls = []
    
    # Look for various patterns found in Google Photos pages
    patterns = [
        r'"imageUris":\["([^"]+)"',  # imageUris pattern
        r'"url":"([^"]*(?:lh3\.googleusercontent|photos)[^"]*)"',  # URLs from Google
        r'https://lh3\.googleusercontent\.com/[^"<>\s]+'  # Direct googleusercontent URLs
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content)
        image_urls.extend(matches)
    
    if not image_urls:
        return None
    
    # Unescape URLs
    image_urls = [url.replace('\\/', '/') for url in image_urls]
    
    # Filter out thumbnails and profile pictures
    # Profile pictures typically have s64-p-no, s32-p-no, s40-p-no etc
    # Main images typically have larger dimensions or no size parameter
    main_images = [url for url in image_urls if not re.search(r's\d{1,3}-p-no|w64|h64|s40|s32|s24', url)]
    
    if main_images:
        # Return the first non-thumbnail image (usually the largest)
        return main_images[0]
    
    # If all images are filtered, return the largest one by analyzing size params
    if image_urls:
        # Sort by size parameter (e.g., s1200, s800, s64) - larger numbers first
        def get_size(url):
            match = re.search(r's(\d+)', url)
            return int(match.group(1)) if match else 0
        
        image_urls.sort(key=get_size, reverse=True)
        return image_urls[0]
    
    return None
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python prep-image.py <input.jpg|URL> output.jpg")
        sys.exit(1)
    input_source = sys.argv[1]
    output_path = sys.argv[2]
    
    # Check if input is a URL or file path
    if input_source.startswith(('http://', 'https://')):
        # Download image from URL
        try:
            if HAS_REQUESTS:
                response = requests.get(input_source, allow_redirects=True, timeout=10)
                response.raise_for_status()
                html_content = response.text
            else:
                req = Request(input_source, headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req, timeout=10) as response:
                    html_content = response.read().decode('utf-8')
            
            # Check if this is a Google Photos link by looking for image URLs in the HTML
            if 'photos.app.goo.gl' in input_source or 'content-type' not in locals():
                image_url = extract_image_url_from_google_photos(html_content)
                if image_url:
                    print(f"Found image URL: {image_url}")
                    # Download the actual image
                    if HAS_REQUESTS:
                        img_response = requests.get(image_url, allow_redirects=True, timeout=10)
                        img_response.raise_for_status()
                        img_data = img_response.content
                    else:
                        req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urlopen(req, timeout=10) as response:
                            img_data = response.read()
                else:
                    # Not a Google Photos page, treat as direct image data
                    if HAS_REQUESTS:
                        response = requests.get(input_source, allow_redirects=True, timeout=10)
                        response.raise_for_status()
                        img_data = response.content
                    else:
                        req = Request(input_source, headers={'User-Agent': 'Mozilla/5.0'})
                        with urlopen(req, timeout=10) as response:
                            img_data = response.read()
            else:
                img_data = html_content.encode('utf-8')
            
            img = Image.open(BytesIO(img_data))
        except Exception as e:
            print(f"Error downloading image from URL: {e}")
            sys.exit(1)
        
        # Resize and save
        width_percent = (1920 / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((1920, height_size), Image.Resampling.BICUBIC)
        img.save(output_path, 'JPEG', quality=85)
    else:
        # Use file path
        prep_image(input_source, output_path)