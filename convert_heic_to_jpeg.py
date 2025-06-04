#!/usr/bin/env python3
import os
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()

def convert_heic_to_jpeg(input_path, output_path=None, quality=95):
    """Convert a HEIC file to JPEG format."""
    if output_path is None:
        # Generate output path by replacing extension
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.jpg"
    
    # Open and convert the image
    with Image.open(input_path) as img:
        # Convert to RGB if necessary (HEIC might have alpha channel)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save as JPEG
        img.save(output_path, 'JPEG', quality=quality)
        print(f"Converted: {input_path} -> {output_path}")
    
    return output_path

def main():
    # Get current directory
    current_dir = os.getcwd()
    
    # Find all HEIC files
    heic_files = [f for f in os.listdir(current_dir) if f.lower().endswith(('.heic', '.heif'))]
    
    if not heic_files:
        print("No HEIC files found in the current directory.")
        return
    
    print(f"Found {len(heic_files)} HEIC file(s) to convert:")
    for file in heic_files:
        print(f"  - {file}")
    
    # Convert each file
    converted_count = 0
    for heic_file in heic_files:
        try:
            input_path = os.path.join(current_dir, heic_file)
            output_filename = os.path.splitext(heic_file)[0] + ".jpg"
            output_path = os.path.join(current_dir, output_filename)
            
            convert_heic_to_jpeg(input_path, output_path)
            
            # Delete the original HEIC file
            os.remove(input_path)
            print(f"  Deleted original: {heic_file}")
            
            converted_count += 1
        except Exception as e:
            print(f"Error converting {heic_file}: {e}")
    
    print(f"\nConversion complete! {converted_count}/{len(heic_files)} files converted.")
    print("Original HEIC files have been deleted.")

if __name__ == "__main__":
    main()