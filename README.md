# HEIC to JPEG Converter

A simple Python script to convert HEIC/HEIF image files to JPEG format.

## Features

- Batch converts all HEIC files in the current directory
- Automatically deletes original HEIC files after successful conversion
- Preserves original filenames (only changes extension)
- High-quality JPEG output (95% quality)

## Requirements

- Python 3.6+
- Pillow
- pillow-heif

## Installation

1. Clone this repository or download the script
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place the script in the directory containing your HEIC files
2. Run the script:

```bash
python convert_heic_to_jpeg.py
```

The script will:
- Find all HEIC files in the current directory
- Convert each file to JPEG format
- Save the JPEG files in the same directory
- Delete the original HEIC files

## Note

⚠️ **Warning**: This script automatically deletes the original HEIC files after conversion. Make sure you have backups if you want to keep the originals.

## License

MIT License