import qrcode

url = "http://192.168.1.164:5000/"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

qr.make_image(fill_color="black", back_color="white").save("qrcode.png")
