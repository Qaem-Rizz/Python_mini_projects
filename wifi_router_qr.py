import qrcode

def generate_hotspot_qr():
    print("--- Mobile Hotspot/ Router QR Code Generator ---")
    
    # Phone hotspot details:
    ssid = input("Enter your Phone Hotspot/Router's Name (SSID): ").strip()
    password = input("Enter your Password: ").strip()
    
    # Standard Wi-Fi URI format (works for phone hotspots too)
    wifi_string = f"WIFI:S:{ssid};T:WPA;P:{password};;"

    # Generate QR Code
    qr_img = qrcode.make(wifi_string)

    # Save and Show
    filename = f"hotspot_qr_{ssid}.png"
    qr_img.save(filename)
    
    print(f"\nSuccess! Hotspot QR code generated and saved as '{filename}'.")
    
    qr_img.show()

if __name__ == "__main__":
    generate_hotspot_qr()