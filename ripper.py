import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_file(url, folder):
    """Download a file from url to the specified folder"""
    try:
        # Create folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        # Get filename from url
        filename = os.path.join(folder, os.path.basename(urlparse(url).path))
        if not filename.strip():
            return
            
        # Download file
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def rip_website():
    # URL of the website
    url = 'https://www.dogefin.space/'
    
    # Create media folder
    media_folder = 'media'
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
    
    try:
        # Get the webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save the HTML
        with open(os.path.join(media_folder, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Downloaded: index.html")
        
        # Download images
        for img in soup.find_all('img'):
            img_url = urljoin(url, img.get('src', ''))
            if img_url:
                download_file(img_url, media_folder)
                
        # Download CSS files
        for css in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(url, css.get('href', ''))
            if css_url:
                download_file(css_url, media_folder)
                
        # Download JavaScript files
        for script in soup.find_all('script', src=True):
            script_url = urljoin(url, script.get('src', ''))
            if script_url:
                download_file(script_url, media_folder)
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    rip_website()
