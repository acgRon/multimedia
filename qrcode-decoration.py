import requests
from bs4 import BeautifulSoup
import qrcode
from PIL import Image

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


def generate_custom_qrcode(data, output_file="qrcode.png", color="black", bg_color="white"):
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
    
    logo_path = get_channel_thumbnail(data)

    # 生成 QR Code 圖像
    img = qr.make_image(fill_color=color, back_color=bg_color).convert("RGB")
    if logo_path:
            logo = Image.open(logo_path)

            # 調整 logo 尺寸（根據 QR Code 的尺寸）
            qr_width, qr_height = img.size
            logo_size = qr_width // 4  # logo 大小約為 QR Code 的 1/4
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # 計算 logo 的位置並貼到 QR Code 上
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, logo_pos)
    # 儲存 QR Code 圖像
    img.save(output_file)
    print(f"QR Code 已儲存到 {output_file}")

url = 'https://www.youtube.com/@mvllabccu9828'
get_channel_thumbnail(url)

channel_name = url[url.find('@')+1:]


output = f'output/{channel_name}_qrcode.png'



generate_custom_qrcode(url, output)