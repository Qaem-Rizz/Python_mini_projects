import qrcode

def generate_universal_upi_qr():
    print("--- Universal UPI QR Code Generator ---")
    
    # taking inputs from the user to generate a personalized UPI QR code:

    upi_id = input("Enter your UPI ID (e.g., username@paytm): ").strip()
    name = input("Enter your Name (e.g., John Doe): ").strip()
    
    # setting the default amount and message - only if we want to include them in the QR code. If left blank, they will be dynamic.

    amount = input("Enter amount (leave blank if dynamic): ").strip()
    note = input("Enter note/message (leave blank if none): ").strip()

    # making the standard universal qr code format for UPI payments. This format is recognized by all UPI apps.
    upi_url = f"upi://pay?pa={upi_id}&pn={name}"
    
    if amount:
        upi_url += f"&am={amount}"
    if note:
        upi_url += f"&tn={note}"

    # generating a single universal QR code that can be scanned by any UPI app

    qr_img = qrcode.make(upi_url)

    #saving and showing the  generated QR code image:

    image_name = "universal_upi_qr.png"
    qr_img.save(image_name)
    
    print(f"\nSuccess! Universal QR Code generated and saved as '{image_name}'.")
    print("You can scan this single QR code using ANY UPI app (GPay, PhonePe, Paytm, etc.)!")
    
    # Display the QR code image
    qr_img.show()

if __name__ == "__main__":
    generate_universal_upi_qr()