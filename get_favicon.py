import qrcode.image.styledpil
import requests
from bs4 import BeautifulSoup
import qrcode
from PIL import Image
import urllib.parse
import os
import re

favicon_path = "favicon.ico"

def get_favicon(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    icon_link = soup.find("link", rel="icon")
    if not icon_link:
        icon_link = soup.find("link", rel="shortcut icon")
    if icon_link and 'href' in icon_link.attrs:
        icon_url = urllib.parse.urljoin(url, icon_link['href'])
    else:
        icon_url = urllib.parse.urljoin(url, '/favicon.ico')
        
    icon_response = requests.get(icon_url, stream=True)
    if icon_response.status_code == 200:
        with open("favicon.ico", "wb") as file:
            file.write(icon_response.content)
            
        print(f"Favicon 已下載: {icon_url}")
        return favicon_path
    else:
        print("未能找到 Favicon 或下載失敗")
        return None
        
def generate_custom_qrcode(data, output_file="qrcode.png", color="black", bg_color="white", thumbnail_percentage=1/2):
    
    # 建立 QR Code 物件
    qr = qrcode.QRCode(
        version=1,  # 控制 QR Code 的大小，值越高，QR Code 越密集
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 錯誤修正能力（L、M、Q、H）
        box_size=10,  # 每個方塊的像素大小
        border=4,  # 邊框的厚度（單位：方塊）
    )
    
    # 添加資料
    qr.add_data(data)
    qr.make(fit=True)

    # 生成 QR Code 圖像
    #img = qr.make_image(image_factory=qrcode.image.styledpil.StyledPilImage, embeded_image_path=logo_path).convert("RGB")
    img = qr.make_image(fill_color=color, back_color=bg_color).convert("RGBA")
    
    logo_path = get_favicon(data)
    
        
    
    if logo_path:
            logo = Image.open(logo_path).convert("RGBA")
            

            # 調整 logo 尺寸（根據 QR Code 的尺寸）
            qr_width, qr_height = img.size
            logo_size = round(qr_width * thumbnail_percentage)  # logo 大小
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)


            # 計算 logo 的位置並貼到 QR Code 上
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            img.paste(logo, logo_pos, logo)

    else:
        print("找不到可用的logo")
        
    # 儲存 QR Code 圖像
    img.save(output_file) # 儲存 QR Code 圖像
    print(f"QR Code 已儲存到 {output_file}")

url = input("address: ")
folder_path = "output_favicon"

match = re.search(r'://(?:www\.)?([^./]+)', url)
website_name = match.group(1)


    
website_name = urllib.parse.unquote(website_name)

output = f'{folder_path}/{website_name}_qrcode.png'


try:
    os.makedirs(folder_path, exist_ok=True)
except FileExistsError:
    print(f"Folder '{folder_path}' already exists.")


thumbnail_percentage = float(input("thumbnail_percentage(float): "))


generate_custom_qrcode(url, output, thumbnail_percentage=thumbnail_percentage)
