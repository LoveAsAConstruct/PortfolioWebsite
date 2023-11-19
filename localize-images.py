import os
import re
import json
import requests

def find_and_download_images(html_directory, images_directory, image_url_pattern, json_directory, json_images_directory):
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
        print(f"Created directory for HTML images: {images_directory}")
    if not os.path.exists(json_images_directory):
        os.makedirs(json_images_directory)
        print(f"Created directory for JSON images: {json_images_directory}")

    # Process HTML files
    for root, dirs, files in os.walk(html_directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Processing HTML file: {file_path}")
                with open(file_path, 'r+', encoding='utf-8', errors='ignore') as file:
                    contents = file.read()
                    urls = re.findall(image_url_pattern, contents)
                    if urls:
                        print(f"Found {len(urls)} image URLs in {file_path}")
                        download_and_replace_images(urls, images_directory, contents, file, html_directory)
                    else:
                        print("No image URLs found in HTML file.")
    
    # Process JSON files
    process_json_files(json_directory, json_images_directory, image_url_pattern, json_directory)

def download_image(url, directory):
    image_name = url.split('/')[-1]
    image_path = os.path.join(directory, image_name)

    if not os.path.exists(image_path):
        try:
            print(f"Attempting to download image: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                print(f"Successfully downloaded {image_name} to {image_path}")
            else:
                print(f"Failed to download {url}. HTTP status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return None
    else:
        print(f"Image already exists, skipping download: {image_path}")

    return image_path

def process_json_files(json_directory, json_images_directory, image_url_pattern, project_root):
    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"Processing JSON file: {file_path}")
                with open(file_path, 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    modified = False
                    for item in data:
                        if 'imgSrc' in item:
                            img_url = item['imgSrc']
                            print(f"Found imgSrc in JSON: {img_url}")
                            if re.match(image_url_pattern, img_url):
                                print("IMAGE URL MATCH")
                                local_image_path = download_image(img_url, json_images_directory)
                                if local_image_path:
                                    relative_path = os.path.relpath(local_image_path, start=project_root)
                                    item['imgSrc'] = relative_path
                                    modified = True
                                    print(f"Updated imgSrc to {relative_path}")
                    if modified:
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()
                        print(f"Updated image URLs in JSON file: {file_path}")
                    else:
                        print("No matching imgSrc found or updated in JSON file.")

def download_and_replace_images(urls, directory, contents, file_obj, project_root):
    for url in urls:
        print(f"Found URL in HTML: {url}")
        local_image_path = download_image(url, directory)
        if local_image_path:
            relative_path = os.path.relpath(local_image_path, start=project_root)
            contents = contents.replace(url, relative_path)
    file_obj.seek(0)
    file_obj.write(contents)
    file_obj.truncate()
    print("Updated image URLs in HTML file.")

# Usage
project_root = '/Users/isaiahmurray/Documents/Home/homepage'  # Root directory of your project
html_directory = os.path.join(project_root, '')
images_directory = os.path.join(project_root, 'images/Localized')
json_directory = os.path.join(project_root, 'Project Data')
json_images_directory = os.path.join(project_root, 'images/Localized/JSONImages')
image_url_pattern = r'https?://(?:d20kqt4x4odakd\.cloudfront\.net/[^ ]+|\S+\.(?:jpg|jpeg|png|gif|bmp|svg))'  # Updated regex pattern

find_and_download_images(html_directory, images_directory, image_url_pattern, json_directory, json_images_directory)
