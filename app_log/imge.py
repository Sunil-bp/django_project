from PIL import Image

path = r"C:\Users\sunil\Pictures\Capture.PNG"

img = Image.open(path)


new_path =  r"C:\Users\sunil\Pictures\Capture111.PNG"
if img.height > 300 or img.width > 300:
    output_size = (300, 300)
    img.thumbnail(output_size)
    img.save(new_path)
