from flask import Flask, render_template
from PIL import Image
import os

app = Flask(__name__)

def get_image_aspect(filename):
    """Determine if image is landscape, portrait, or square"""
    try:
        with Image.open(os.path.join('static/images', filename)) as img:
            width, height = img.size
            if width > height:
                return 'landscape'
            elif height > width:
                return 'portrait'
            else:
                return 'square'
    except:
        return 'landscape'  # default if can't determine

# Gallery images data
gallery_images = [
    {
        'thumb': f'{i}.jpg',
        'full': f'{i}.jpg',
        'caption': 'Doge Spring Rider'
    }
    for i in range(1, 32)
]

# Update specific entries for GIFs and PNGs
gif_indices = [18, 21, 26]  # GIF files
png_indices = [9]           # PNG files

# Update file extensions and get aspect ratios
for i in range(1, 32):
    ext = '.gif' if i in gif_indices else '.png' if i in png_indices else '.jpg'
    filename = f'{i}{ext}'
    gallery_images[i-1].update({
        'thumb': filename,
        'full': filename,
        'aspect': get_image_aspect(filename)
    })

@app.route('/')
def index():
    return render_template('index.html', images=gallery_images)

if __name__ == '__main__':
    app.run(debug=True) 