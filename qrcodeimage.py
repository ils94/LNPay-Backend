import qrcode
import io
import base64


# Function to generate a QR Code image from the lninvoice and convert that to base64, making it easier to show
# in a webpage
def generate(lninvoice):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(lninvoice)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return qr_code_base64
