from PIL import Image, ImageDraw
import os

output_path = 'mask/mask1.png'

mask_size = 450

image = Image.new('RGB', (mask_size, mask_size), 'black')
draw = ImageDraw.Draw(image)

outlinecolor = int(input('outline color(grayscale): '))
innercolor = int(input('inner color(grayscale): '))
width = int(input('width: '))

draw.ellipse((0, 0, mask_size, mask_size), (innercolor, innercolor, innercolor), outline=(outlinecolor, outlinecolor, outlinecolor), width=width)

index = 1
while os.path.exists(output_path):
    output_path = f'mask/mask{index + 1}.png'
    index += 1
    

image.show()
image.save(output_path)