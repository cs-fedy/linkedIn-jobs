import os
import io
import json
from typing import Tuple
from PIL import Image
import requests


def download_image(download_path, url, file_name):
	download_path = download_path.replace("\n", "")
	if not os.path.isdir(download_path):
		os.makedirs(download_path)
		print("Created folder: " + download_path)

	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
		return True
	except Exception as e:
		print('FAILED -', e)
		return False

def load_urls(file_path) -> Tuple[str, str]:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [(element['picture'], element['name']) for element in data]

if __name__ == '__main__':
    urls = load_urls('employees.json')
    for (url, name) in urls:
        try:
            download_image('downloads', url, name)
        except:
            print(f'=== failed to download {url}')