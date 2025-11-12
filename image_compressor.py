#!/usr/bin/env python3
"""
Image Compressor - Compress PNG, JPG, and JPEG images
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image


def compress_image(input_path, output_path=None, quality=85, max_width=None, max_height=None):
    """
    Compress an image file.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the compressed image (optional)
        quality (int): Compression quality (1-100, default 85)
        max_width (int): Maximum width for resizing (optional)
        max_height (int): Maximum height for resizing (optional)
    
    Returns:
        str: Path to the compressed image
    """
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Check file extension
    supported_formats = ['.png', '.jpg', '.jpeg']
    file_ext = Path(input_path).suffix.lower()
    if file_ext not in supported_formats:
        raise ValueError(f"Unsupported file format: {file_ext}. Supported: {', '.join(supported_formats)}")
    
    # Open image
    try:
        img = Image.open(input_path)
    except Exception as e:
        raise ValueError(f"Error opening image: {e}")
    
    # Resize if dimensions specified
    if max_width or max_height:
        original_width, original_height = img.size
        new_width, new_height = original_width, original_height
        
        if max_width and original_width > max_width:
            ratio = max_width / original_width
            new_width = max_width
            new_height = int(original_height * ratio)
        
        if max_height and new_height > max_height:
            ratio = max_height / new_height
            new_height = max_height
            new_width = int(new_width * ratio)
        
        if (new_width, new_height) != (original_width, original_height):
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Determine output path
    if output_path is None:
        input_file = Path(input_path)
        output_path = input_file.parent / f"{input_file.stem}_compressed{input_file.suffix}"
    
    # Get output file extension
    output_ext = Path(output_path).suffix.lower()
    
    # Convert RGBA to RGB if saving as JPEG
    if img.mode == 'RGBA' and output_ext in ['.jpg', '.jpeg']:
        # Create a white background
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        img = rgb_img
    
    # Save compressed image
    try:
        if output_ext == '.png':
            img.save(output_path, 'PNG', optimize=True)
        else:  # jpg or jpeg
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
    except Exception as e:
        raise ValueError(f"Error saving compressed image: {e}")
    
    return str(output_path)


def get_file_size_mb(file_path):
    """Get file size in megabytes."""
    return os.path.getsize(file_path) / (1024 * 1024)


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description='Compress PNG, JPG, and JPEG images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.jpg
  %(prog)s image.png -o output.png
  %(prog)s image.jpg -q 75
  %(prog)s image.png --max-width 1920 --max-height 1080
        """
    )
    
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('-o', '--output', help='Output image file path (default: input_compressed.ext)')
    parser.add_argument('-q', '--quality', type=int, default=85, 
                        help='Compression quality for JPEG (1-100, default: 85)')
    parser.add_argument('--max-width', type=int, help='Maximum width for resizing')
    parser.add_argument('--max-height', type=int, help='Maximum height for resizing')
    
    args = parser.parse_args()
    
    # Validate quality
    if args.quality < 1 or args.quality > 100:
        print("Error: Quality must be between 1 and 100", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Get original file size
        original_size = get_file_size_mb(args.input)
        
        # Compress image
        output_path = compress_image(
            args.input,
            args.output,
            args.quality,
            args.max_width,
            args.max_height
        )
        
        # Get compressed file size
        compressed_size = get_file_size_mb(output_path)
        
        # Calculate compression ratio
        reduction = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0
        
        # Print results
        print(f"✓ Image compressed successfully!")
        print(f"  Input:  {args.input} ({original_size:.2f} MB)")
        print(f"  Output: {output_path} ({compressed_size:.2f} MB)")
        print(f"  Size reduction: {reduction:.1f}%")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
