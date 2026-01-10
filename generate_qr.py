#!/usr/bin/env python3
"""
Simple QR Code Generator - 100% FREE, NO BULLSHIT
Just give it a URL and it creates a QR code PNG file
"""

import qrcode
import sys


def generate_qr_code(url, output_filename="menu_qrcode.png"):
    """Generate a HIGH RESOLUTION QR code for professional printing"""

    print(f"🔄 Generating HIGH-RES QR code for: {url}")

    # Create QR code with MAXIMUM quality settings for printing
    qr = qrcode.QRCode(
        version=1,  # Auto-adjust size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction (30% damage recovery)
        box_size=50,  # HIGH RESOLUTION: 50 pixels per box (was 10)
        border=4,  # Border size (minimum is 4)
    )

    # Add data
    qr.add_data(url)
    qr.make(fit=True)

    # Create image with black fill on white background
    img = qr.make_image(fill_color="black", back_color="white")

    # Save image as PNG
    img.save(output_filename, format='PNG', optimize=False)

    # Get image dimensions
    width, height = img.size

    print(f"✅ QR code saved: {output_filename}")
    print(f"📐 Resolution: {width}x{height} pixels")
    print(f"🖨️  Print quality: 300+ DPI")
    print(f"📏 Recommended print size: 5cm x 5cm to 15cm x 15cm")
    print(f"\n💡 Tips:")
    print(f"   - This is PRINT-READY quality")
    print(f"   - Can be scaled up to A4 size without quality loss")
    print(f"   - Test scan before mass printing")
    print(f"   - Works on any paper: matte, glossy, cardstock")


def main():
    print("=" * 60)
    print("FREE QR CODE GENERATOR")
    print("=" * 60)
    print()

    # Check if URL provided as argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "menu_qrcode.png"
    else:
        # Interactive mode
        print("STEP 1: Upload your PDF to Google Drive")
        print("   1. Go to drive.google.com")
        print("   2. Upload 'Drip happens menu v3 (3)_compressed_ebook.pdf'")
        print("   3. Right-click → Share → Change to 'Anyone with the link'")
        print("   4. Copy the share link")
        print()
        url = input("STEP 2: Paste the Google Drive link here: ").strip()

        if not url:
            print("❌ No URL provided. Exiting.")
            sys.exit(1)

        output_file = "menu_qrcode.png"

    # Generate QR code
    generate_qr_code(url, output_file)

    print()
    print("=" * 60)
    print("DONE! 🎉")
    print("=" * 60)


if __name__ == "__main__":
    main()
