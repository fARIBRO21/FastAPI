import io
from fastapi import FastAPI
from PIL import Image, ImageFilter
from pathlib import Path
import concurrent.futures
import zipfile
from fastapi.responses import FileResponse
import requests
app = FastAPI()
def process_image(url, count):
	try:
		response = requests.get(url)
		image = Image.open(io.BytesIO(response.content))
		image = image.filter(ImageFilter.GaussianBlur(1))
		temp_image_path =Path(f"temp_{count}.jpg")
		image.save(temp_image_path)

	except Exception as e:
		print(e)

def add_images_to_zip(zipf):
	try:
		for i in range(10):
			image_path = Path(f"temp_{i}.jpg")
			zipf.write(image_path)
			image_path.unlink() 
	except Exception as e:
		print(e)


@app.get("/download")
async def uploadfile():
	try:
		url = "https://picsum.photos/200/300"
		list = [] 
		zip_file_path = Path("processed_images.zip")
		with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
			with concurrent.futures.ProcessPoolExecutor() as executor:
				for i in range(10):
					futures = executor.submit(process_image, url, i) 
					print(futures)
					list.append(futures)
				concurrent.futures.wait(list)
				add_images_to_zip(zipf)
		return FileResponse(zip_file_path, headers={"Content-Disposition": "attachment; filename=processed_images.zip"})
	except Exception as e:
		print(e)
		return {"message": e}
