import qrcode
from PIL import Image
import numpy as np

# 定義生成 QR Code 的內容（例如一個 URL 或文字）
data = "https://cs.ccu.edu.tw/p/404-1094-6474.php?Lang=zh-tw"

# 設定 QR Code 的參數
qr = qrcode.QRCode(
    version=1,  # 控制 QR Code 的大小（1 是最小的，40 是最大的）
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 設定容錯率
    box_size=10,  # 每個方塊的像素大小
    border=4,  # 邊框的厚度（最小為4）
)

# 將資料添加到 QR Code
qr.add_data(data)
qr.make(fit=True)

# 生成 QR Code 的影像
img = qr.make_image(fill_color="black", back_color="white")

# 載入背景圖片
background_path = "4.jpg"  # 替換為你的背景圖片檔案路徑
logo_path = "4.jpg"  # 替換為要放置在中央的圖片（例如 logo）

try:
    # 載入背景圖片
    img_bg = Image.open(background_path)
    
    # 確保背景圖片大小與 QR Code 匹配
    img_bg = img_bg.resize(img.size)

    # 轉換背景圖片為 RGB
    img_bg = img_bg.convert("RGB")
    
    # 提取背景圖片的平均顏色
    img_array = np.array(img_bg)
    avg_color = np.mean(img_array, axis=(0, 1))  # 取得平均顏色（RGB）

    # 生成 QR Code，將平均顏色應用於 QR Code 的每個填充區塊
    img = img.convert("RGB")
    pixels = img.load()

    # 根據背景顏色改變 QR Code 方塊的顏色
    for i in range(img.width):
        for j in range(img.height):
            if pixels[i, j] == (0, 0, 0):  # 只改變黑色的區塊
                pixels[i, j] = tuple(map(int, avg_color))  # 將平均顏色應用到這些區塊

    # 載入並處理要貼中間的圖片（例如 logo）
    logo = Image.open(logo_path)
    logo = logo.convert("RGBA")  # 確保 logo 具有透明通道

    # 放大 logo，這裡將 logo 的大小設定為 100（可以根據需要調整）
    logo_size = 100  # 增大 logo 的大小，這裡的 100 是像素大小
    logo = logo.resize((logo_size, logo_size))

    # 計算 logo 位置並將其貼到 QR Code 中
    img_width, img_height = img.size
    logo_position = (
        (img_width - logo_size) // 2,
        (img_height - logo_size) // 2,
    )

    # 在原始 QR Code 圖像上貼上 logo，使用透明度處理
    img = img.convert("RGBA")  # 轉換 QR Code 為 RGBA 格式，這樣可以處理透明通道
    img.paste(logo, logo_position, logo)  # 使用 logo 的透明度作為遮罩

    # 儲存最終結果
    img.save("logo.png")
    print("QR Code 已儲存為 logo.png")

except FileNotFoundError:
    print("圖片檔案未找到，無法進行處理。")
