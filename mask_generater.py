from PIL import Image, ImageDraw
import os

folder_path = "mask"
output_path = f'{folder_path}/mask1.png'

mask_size = 450

image = Image.new('RGB', (mask_size, mask_size), 'black')
draw = ImageDraw.Draw(image)

outlinecolor = int(input('outline color(grayscale): '))
innercolor = int(input('inner color(grayscale): '))
width = int(input('width: '))

draw.ellipse((0, 0, mask_size, mask_size), (innercolor, innercolor, innercolor), outline=(outlinecolor, outlinecolor, outlinecolor), width=width)

try:
    os.makedirs(folder_path, exist_ok=True)
except FileExistsError:
    print(f"Folder '{folder_path}' already exists.")


index = 1
while os.path.exists(output_path):
    output_path = f'mask/mask{index + 1}.png'
    index += 1
    

image.show()
image.save(output_path)
