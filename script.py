import os
from tkinter import Tk, simpledialog
from tkinter.filedialog import askopenfilename
from PIL import Image

def image_compressor(file_path, quality):
    try:
        # Verify file type
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.bmp')):
            with Image.open(file_path) as img:
                # Output file path
                base, ext = os.path.splitext(file_path)
                output_path = f"{base}_compressed{ext}"

                # Save image with chosen quality
                img.save(output_path, quality=quality, optimize=True)

            print(f"Image compressed and saved as: {output_path}")
        else:
            print("Unsupported image format!")

    except Exception as e:
        print(f"Error compressing image: {e}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the main tkinter window

    print("Select an image file to compress")
    file_path = askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.tiff *.bmp")]
    )

    if file_path:
        # Ask user for desired quality (1–100)
        quality = simpledialog.askinteger(
            "Compression Quality",
            "Enter quality (1 = lowest, 500 = highest):",
            minvalue=1,
            maxvalue=500
        )

        if quality is not None:
            image_compressor(file_path, quality)
        else:
            print("Compression cancelled by user.")
    else:
        print("No file selected.")
