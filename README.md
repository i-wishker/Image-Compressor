# Image-Compressor

Compresses your images! A simple and efficient Python tool to compress PNG, JPG, and JPEG images.

## Features

- 🖼️ Supports PNG, JPG, and JPEG formats
- 🗜️ Adjustable compression quality for JPEG files
- 📏 Optional image resizing (maintain aspect ratio)
- 💾 Automatic file size reduction reporting
- ⚡ Fast and easy to use

## Installation

1. Clone this repository:
```bash
git clone https://github.com/i-wishker/Image-Compressor.git
cd Image-Compressor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Compress an image with default settings (quality: 85 for JPEG):
```bash
python image_compressor.py image.jpg
```

This will create a compressed image named `image_compressed.jpg` in the same directory.

### Specify Output File

```bash
python image_compressor.py image.png -o output.png
```

### Adjust Compression Quality (JPEG only)

Quality ranges from 1 (lowest quality, smallest file) to 100 (highest quality, largest file):
```bash
python image_compressor.py image.jpg -q 75
```

### Resize Images

Resize while maintaining aspect ratio:
```bash
python image_compressor.py image.png --max-width 1920 --max-height 1080
```

### Combined Options

```bash
python image_compressor.py photo.jpg -o compressed_photo.jpg -q 80 --max-width 1920
```

## Examples

**Example 1:** Compress a JPEG with 70% quality
```bash
python image_compressor.py vacation.jpg -q 70
```

**Example 2:** Compress and resize a PNG
```bash
python image_compressor.py screenshot.png --max-width 1280
```

**Example 3:** Convert RGBA PNG to JPEG with compression
```bash
python image_compressor.py image.png -o image.jpg -q 85
```

## Command-Line Options

```
usage: image_compressor.py [-h] [-o OUTPUT] [-q QUALITY] [--max-width MAX_WIDTH]
                          [--max-height MAX_HEIGHT] input

positional arguments:
  input                 Input image file path

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output image file path (default: input_compressed.ext)
  -q QUALITY, --quality QUALITY
                        Compression quality for JPEG (1-100, default: 85)
  --max-width MAX_WIDTH
                        Maximum width for resizing
  --max-height MAX_HEIGHT
                        Maximum height for resizing
```

## Requirements

- Python 3.6+
- Pillow (PIL Fork)

## License

MIT License - see [LICENSE](LICENSE) file for details
