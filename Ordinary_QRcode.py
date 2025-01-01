import qrcode

# 產生 QR Code 的內容
data = "https://www026190.ccu.edu.tw/evaluation/001.php"

# 設定 QR Code 的參數
qr = qrcode.QRCode(
    version=1,  # 控制 QR Code 的大小（1 ~ 40），數字越大，QR Code 越大
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # 容錯率（L、M、Q、H）
    box_size=10,  # 每個格子的像素數
    border=4,  # QR Code 的邊框厚度（最小為4）
)

# 將資料加入 QR Code
qr.add_data(data)
qr.make(fit=True)

# 產生影像
img = qr.make_image(fill_color="black", back_color="white")

# 儲存影像
img.save("qrcode.png")

print("QR Code 已成功生成並儲存為 'qrcode.png'")
