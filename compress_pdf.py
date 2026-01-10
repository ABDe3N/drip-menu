#!/usr/bin/env python3
"""
PDF Compression Script
Compresses PDF files to under 20MB with minimal quality loss
"""

import os
import subprocess
import sys
from pathlib import Path


def get_file_size_mb(file_path):
    """Get file size in megabytes"""
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb


def compress_pdf_ghostscript(input_path, output_path, quality='ebook'):
    """
    Compress PDF using Ghostscript

    Quality levels:
    - 'screen': Lower quality (72 DPI) - smallest file
    - 'ebook': Medium quality (150 DPI) - balanced (RECOMMENDED)
    - 'printer': High quality (300 DPI) - larger file
    - 'prepress': Highest quality (300 DPI) - largest file
    """

    print(f"🔄 Compressing PDF with quality level: {quality}")

    # Ghostscript command
    gs_command = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{quality}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        '-dDetectDuplicateImages=true',
        '-dCompressFonts=true',
        '-r150',  # Resolution: 150 DPI (good balance)
        f'-sOutputFile={output_path}',
        input_path
    ]

    try:
        # Run Ghostscript
        result = subprocess.run(
            gs_command,
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Ghostscript not found! Install it first:")
        print("   macOS: brew install ghostscript")
        print("   Linux: sudo apt-get install ghostscript")
        print("   Windows: Download from https://www.ghostscript.com/")
        return False


def main():
    # Input file
    input_file = "/Users/ibnabdeen/Dev/kalemat/Drip happens menu v3 (3).pdf"

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File not found: {input_file}")
        sys.exit(1)

    # Get original size
    original_size = get_file_size_mb(input_file)
    print(f"📄 Original file size: {original_size:.2f} MB")

    # Output file
    base_name = Path(input_file).stem
    output_dir = Path(input_file).parent

    # Target: under 20MB
    target_size_mb = 20

    # Try different quality levels
    quality_levels = [
        ('ebook', f"{output_dir}/{base_name}_compressed_ebook.pdf"),
        ('screen', f"{output_dir}/{base_name}_compressed_screen.pdf"),
    ]

    print(f"\n🎯 Target: Under {target_size_mb} MB\n")

    success_file = None

    for quality, output_file in quality_levels:
        print(f"{'='*60}")
        print(f"Trying quality level: {quality.upper()}")
        print(f"{'='*60}")

        # Compress
        if compress_pdf_ghostscript(input_file, output_file, quality):
            compressed_size = get_file_size_mb(output_file)
            compression_ratio = (1 - compressed_size / original_size) * 100

            print(f"✅ Compressed file size: {compressed_size:.2f} MB")
            print(f"📉 Compression ratio: {compression_ratio:.1f}%")

            if compressed_size <= target_size_mb:
                print(f"🎉 SUCCESS! File is under {target_size_mb} MB")
                success_file = output_file
                break
            else:
                print(f"⚠️  Still too large ({compressed_size:.2f} MB > {target_size_mb} MB)")
                if quality == 'ebook':
                    print("   Trying lower quality...")
        else:
            print(f"❌ Compression failed for quality level: {quality}")

        print()

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    if success_file:
        final_size = get_file_size_mb(success_file)
        print(f"✅ Compressed file created: {success_file}")
        print(f"📊 Original: {original_size:.2f} MB → Compressed: {final_size:.2f} MB")
        print(f"💾 Space saved: {original_size - final_size:.2f} MB ({(1 - final_size/original_size)*100:.1f}%)")
    else:
        print("❌ Could not compress file to under 20MB with acceptable quality")
        print("💡 Suggestions:")
        print("   1. Use the 'screen' quality version for web use")
        print("   2. Consider splitting the menu into multiple PDFs")
        print("   3. Reduce image resolution in the source document")


if __name__ == "__main__":
    main()
