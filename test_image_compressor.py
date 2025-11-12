#!/usr/bin/env python3
"""
Test suite for image_compressor.py
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from PIL import Image

# Add the parent directory to the path to import image_compressor
sys.path.insert(0, os.path.dirname(__file__))
import image_compressor


def create_test_images(test_dir):
    """Create test images for testing."""
    # PNG image
    img_png = Image.new('RGB', (200, 200), color='red')
    png_path = os.path.join(test_dir, 'test.png')
    img_png.save(png_path, quality=95)
    
    # JPG image
    img_jpg = Image.new('RGB', (300, 300), color='blue')
    jpg_path = os.path.join(test_dir, 'test.jpg')
    img_jpg.save(jpg_path, quality=95)
    
    # JPEG image
    img_jpeg = Image.new('RGB', (250, 250), color='green')
    jpeg_path = os.path.join(test_dir, 'test.jpeg')
    img_jpeg.save(jpeg_path, quality=95)
    
    # RGBA PNG image
    img_rgba = Image.new('RGBA', (200, 200), color=(255, 0, 0, 128))
    rgba_path = os.path.join(test_dir, 'test_rgba.png')
    img_rgba.save(rgba_path)
    
    return png_path, jpg_path, jpeg_path, rgba_path


def test_compress_png():
    """Test PNG compression."""
    print("Testing PNG compression...")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = tmpdir
        png_path, _, _, _ = create_test_images(test_dir)
        
        # Compress PNG
        output = image_compressor.compress_image(png_path)
        
        # Verify output exists
        assert os.path.exists(output), f"Output file not created: {output}"
        
        # Verify output is smaller (or similar size for optimized images)
        original_size = os.path.getsize(png_path)
        compressed_size = os.path.getsize(output)
        assert compressed_size <= original_size, "Compressed file is larger than original"
        
        print("  ✓ PNG compression passed")


def test_compress_jpg():
    """Test JPG compression."""
    print("Testing JPG compression...")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = tmpdir
        _, jpg_path, _, _ = create_test_images(test_dir)
        
        # Compress JPG with quality 70
        output = image_compressor.compress_image(jpg_path, quality=70)
        
        # Verify output exists
        assert os.path.exists(output), f"Output file not created: {output}"
        
        # Verify output is smaller
        original_size = os.path.getsize(jpg_path)
        compressed_size = os.path.getsize(output)
        assert compressed_size < original_size, "Compressed file is not smaller than original"
        
        print("  ✓ JPG compression passed")


def test_compress_jpeg():
    """Test JPEG compression."""
    print("Testing JPEG compression...")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = tmpdir
        _, _, jpeg_path, _ = create_test_images(test_dir)
        
        # Compress JPEG
        output = image_compressor.compress_image(jpeg_path)
        
        # Verify output exists
        assert os.path.exists(output), f"Output file not created: {output}"
        
        print("  ✓ JPEG compression passed")


def test_custom_output():
    """Test custom output path."""
    print("Testing custom output path...")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = tmpdir
        png_path, _, _, _ = create_test_images(test_dir)
        
        custom_output = os.path.join(test_dir, 'custom_output.png')
        output = image_compressor.compress_image(png_path, output_path=custom_output)
        
        assert output == custom_output, f"Output path mismatch: {output} != {custom_output}"
        assert os.path.exists(custom_output), f"Custom output file not created: {custom_output}"
        
        print("  ✓ Custom output path passed")


def test_resize():
    """Test image resizing."""
    print("Testing image resizing...")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = tmpdir
        png_path, _, _, _ = create_test_images(test_dir)
        
        # Resize to max width 100
        output = image_compressor.compress_image(png_path, max_width=100)
        
        # Verify output exists and is resized
        assert os.path.exists(output), f"Output file not created: {output}"
        
        img = Image.open(output)
        assert img.width == 100, f"Image width not resized: {img.width} != 100"
        assert img.height == 100, f"Image height not maintained aspect ratio"
        
        print("  ✓ Image resizing passed")


def test_rgba_to_jpeg():
    """Test RGBA PNG to JPEG conversion."""
    print("Testing RGBA to JPEG conversion...")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = tmpdir
        _, _, _, rgba_path = create_test_images(test_dir)
        
        # Convert RGBA to JPEG
        jpeg_output = os.path.join(test_dir, 'rgba_converted.jpg')
        output = image_compressor.compress_image(rgba_path, output_path=jpeg_output)
        
        # Verify output exists
        assert os.path.exists(output), f"Output file not created: {output}"
        
        # Verify it's a valid JPEG
        img = Image.open(output)
        assert img.mode == 'RGB', f"JPEG should be RGB mode, got {img.mode}"
        
        print("  ✓ RGBA to JPEG conversion passed")


def test_unsupported_format():
    """Test error handling for unsupported format."""
    print("Testing unsupported format error handling...")
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, 'test.bmp')
        
        # Create a BMP file
        img = Image.new('RGB', (100, 100), color='red')
        img.save(test_file)
        
        try:
            image_compressor.compress_image(test_file)
            assert False, "Should have raised ValueError for unsupported format"
        except ValueError as e:
            assert "Unsupported file format" in str(e)
        
        print("  ✓ Unsupported format error handling passed")


def test_nonexistent_file():
    """Test error handling for nonexistent file."""
    print("Testing nonexistent file error handling...")
    try:
        image_compressor.compress_image('/tmp/nonexistent_image_12345.png')
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass
    
    print("  ✓ Nonexistent file error handling passed")


def run_tests():
    """Run all tests."""
    print("Running image_compressor tests...\n")
    
    tests = [
        test_compress_png,
        test_compress_jpg,
        test_compress_jpeg,
        test_custom_output,
        test_resize,
        test_rgba_to_jpeg,
        test_unsupported_format,
        test_nonexistent_file,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
