import qrcode.image.styledpil
import requests
from bs4 import BeautifulSoup
import qrcode
from PIL import Image
import os
import numpy as np
import urllib.parse

thumbnail_path = "channel_thumbnail.jpg"

def get_channel_thumbnail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    thumbnail_meta  = soup.find("meta", property="og:image")
    if not thumbnail_meta :
        print("not thing there!")
    else:
        ch_icon = requests.get(thumbnail_meta['content']).content
        with open(thumbnail_path, "wb") as file:
            file.write(ch_icon)
    return thumbnail_path

def generate_custom_qrcode(data, output_file="qrcode.png", color="black", bg_color="white", thumbnail_percentage=1/2, mask_path=None):
    
    # 建立 QR Code 物件
    qr = qrcode.QRCode(
        version=1,  # 控制 QR Code 的大小，值越高，QR Code 越密集
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 錯誤修正能力（L、M、Q、H）
        box_size=10,  # 每個方塊的像素大小
        border=4,  # 邊框的厚度（單位：方塊）
    )
    
    logo_path = get_channel_thumbnail(data)

    # 添加資料
    qr.add_data(data)
    qr.make(fit=True)

    # 生成 QR Code 圖像
    #img = qr.make_image(image_factory=qrcode.image.styledpil.StyledPilImage, embeded_image_path=logo_path).convert("RGB")
    img = qr.make_image(fill_color=color, back_color=bg_color).convert("RGB")
    if logo_path:
            logo = Image.open(logo_path)

            # 調整 logo 尺寸（根據 QR Code 的尺寸）
            qr_width, qr_height = img.size
            logo_size = round(qr_width * thumbnail_percentage)  # logo 大小
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # 計算 logo 的位置並貼到 QR Code 上
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            if mask_path:
                mask = Image.open(mask_path).convert("L")
                mask = mask.resize((logo_size, logo_size))
                img.paste(logo, logo_pos, mask)
            else:
                img.paste(logo, logo_pos)

    # 儲存 QR Code 圖像
    
    img.save(output_file)
    
    print(f"QR Code 已儲存到 {output_file}")
    
def add_center(data, img, output_file="qrcode.png", thumbnail_percentage=1/2, mask_path=None):
    logo_path = get_channel_thumbnail(data)
    
    if logo_path:
            logo = Image.open(logo_path)

            # 調整 logo 尺寸（根據 QR Code 的尺寸）
            qr_width, qr_height = img.size
            logo_size = round(qr_width * thumbnail_percentage)  # logo 大小
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # 計算 logo 的位置並貼到 QR Code 上
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            if mask_path:
                mask = Image.open(mask_path).convert("L")
                mask = mask.resize((logo_size, logo_size))
                img.paste(logo, logo_pos, mask)
            else:
                img.paste(logo, logo_pos)

    # 儲存 QR Code 圖像
    
    img.save(output_file)
    
def generate_custom_background_qrcode(data, output_file="qrcode.png", color="black", bg_color="white"):
    # 建立 QR Code 物件
    qr = qrcode.QRCode(
        version=5,  # 控制 QR Code 的大小，值越高，QR Code 越密集
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 錯誤修正能力（L、M、Q、H）
        box_size=10,  # 每個方塊的像素大小
        border=2,  # 邊框的厚度（單位：方塊）
    )

    # 添加資料
    qr.add_data(data)
    qr.make(fit=True)
    
    logo_path = get_channel_thumbnail(data)

    # 生成 QR Code 圖像
    img = qr.make_image(fill_color=color, back_color=bg_color).convert("RGB")
    if img.mode == "RGBA":
        img = img.convert("RGB")
        #print("QRcode轉成RGBA")
    #做出背景版本的QR Code
    if logo_path:
        logo = Image.open(logo_path)
        # 調整 logo 尺寸（根據 QR Code 的尺寸）
        qr_width, qr_height = img.size
        logo = logo.resize((qr_width, qr_height), Image.LANCZOS)
        if logo.mode == "RGBA":
            logo = logo.convert("RGB")
            #print("logo轉成RGBA")
        qr_array = np.array(img)
        bg_array = np.array(logo)
        avg_color = np.mean(bg_array, axis=(0, 1))
                
        # 創建半透明 QR Code 的效果
        for y in range(qr_array.shape[0]):
            for x in range(qr_array.shape[1]):
                # 如果是白色模塊（檢查 RGB 值是否為白色）
                if qr_array[y, x, 0] == 255:
                    r = bg_array[y, x, 0].astype(np.int32)
                    g = bg_array[y, x, 1].astype(np.int32)
                    b = bg_array[y, x, 2].astype(np.int32)
                    r = (r + 255)/2
                    g = (g + 255)/2
                    b = (b + 255)/2
                    qr_array[y, x] = (r, g, b)
                    '''qr_array[y, x] = (bg_array[y, x, 0],  # 使用背景的顏色
                                    bg_array[y, x, 1], 
                                    bg_array[y, x, 2], 
                                    80)  # 設定透明度（0-255，150為半透明）'''
                # 如果是黑色模塊（檢查 RGB 值是否為黑色）
                if qr_array[y, x, 0] == 0:
                    #bg_array[y, x] = bg_array[y, x] / 4
                    #qr_array[y, x] = bg_array[y, x]
                    r = bg_array[y, x, 0].astype(np.int32)
                    g = bg_array[y, x, 1].astype(np.int32)
                    b = bg_array[y, x, 2].astype(np.int32)
                    r = r/3 + avg_color[0]/6
                    g = g/3 + avg_color[0]/6
                    b = b/3 + avg_color[0]/6
                    qr_array[y, x] = (r, g, b)
                    
                    
        bg_qr = Image.fromarray(qr_array)
        #bg_qr.show()
        name = output_file[:output_file.find('.')]
        bg_qr.save(f"{name}_bg.png")
        #styled_qr.save("background_qrcode.png")
        return bg_qr

url = input("youtube channal address: ")
get_channel_thumbnail(url)

folder_path = "output"
channel_name_index = url.find('@')
if channel_name_index > 0:
    channel_name = url[channel_name_index+1:]
else:
    channel_name = url[url.rfind('/')+1:]


channel_name = urllib.parse.unquote(channel_name)

output = f'{folder_path}/{channel_name}_qrcode.png'
output2 = f'{folder_path}/{channel_name}_qrcode_cb.png'

mask_path = input("using mask: ")
if mask_path:
    mask_path = f"mask/mask{mask_path}.png"
else:   
    mask_path = None

try:
    os.makedirs(folder_path, exist_ok=True)
except FileExistsError:
    print(f"Folder '{folder_path}' already exists.")


thumbnail_percentage = float(input("thumbnail_percentage(float): "))


generate_custom_qrcode(url, output, thumbnail_percentage=thumbnail_percentage, mask_path=mask_path)
bg_qr = generate_custom_background_qrcode(url, output)
add_center(url, bg_qr, output2, thumbnail_percentage=thumbnail_percentage, mask_path=mask_path)
