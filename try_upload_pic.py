import base64
from main_folder.models import MenuPicture

with open('image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

img = MenuPicture(img=image_data, name=filename, mimetype=mimetype)
