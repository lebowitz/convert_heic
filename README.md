# HEIC to JPEG Converter

A powerful command-line tool to convert HEIC/HEIF image files to JPEG format with advanced features including parallel processing, comprehensive logging, and flexible output options.

## Features

- **Flexible Input Options**: Convert individual files, directories, or use recursive search
- **Parallel Processing**: Multi-threaded conversion for faster batch processing
- **Advanced Logging**: Structured logging with multiple verbosity levels and file output
- **Progress Tracking**: Visual progress bar for batch conversions
- **Dry Run Mode**: Preview operations before executing
- **Customizable Output**: Control output directory, filename suffixes, and JPEG quality
- **Safe Operation**: Option to preserve original files or force overwrite existing outputs
- **Colored Terminal Output**: Enhanced readability with color-coded log messages

## Requirements

- Python 3.6+
- Pillow
- pillow-heif
- tqdm
- colorlog

## Installation

1. Clone this repository or download the script
2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Convert all HEIC files in the current directory:
```bash
python convert_heic_to_jpeg.py
```

Convert specific files:
```bash
python convert_heic_to_jpeg.py image1.heic image2.heic
```

### Advanced Options

#### Output Control
```bash
# Specify output directory
python convert_heic_to_jpeg.py -o converted/

# Add suffix to output filenames
python convert_heic_to_jpeg.py -s "_converted"

# Set JPEG quality (1-100, default: 95)
python convert_heic_to_jpeg.py --quality 85

# Force overwrite existing files
python convert_heic_to_jpeg.py -f
```

#### Processing Options
```bash
# Process directories recursively
python convert_heic_to_jpeg.py -r /path/to/photos

# Delete original files after conversion
python convert_heic_to_jpeg.py -d

# Use parallel processing (4 threads)
python convert_heic_to_jpeg.py -j 4

# Dry run - preview without converting
python convert_heic_to_jpeg.py --dry-run
```

#### Display and Logging
```bash
# Increase verbosity
python convert_heic_to_jpeg.py -v        # Info level
python convert_heic_to_jpeg.py -vv       # Debug level

# Quiet mode - only show errors
python convert_heic_to_jpeg.py -q

# Show progress bar
python convert_heic_to_jpeg.py --progress

# Save logs to file
python convert_heic_to_jpeg.py --log-file conversion.log

# Disable colored output
python convert_heic_to_jpeg.py --no-color
```

### Example Commands

Convert all HEIC files recursively with progress bar and 4 threads:
```bash
python convert_heic_to_jpeg.py -r /photos -j 4 --progress
```

Preview conversion with verbose output:
```bash
python convert_heic_to_jpeg.py --dry-run -v
```

Convert to specific directory with custom quality and logging:
```bash
python convert_heic_to_jpeg.py -o output/ --quality 90 --log-file convert.log -v
```

## Command Line Options

```
positional arguments:
  paths                 Files or directories to process (default: current directory)

output options:
  -o DIR, --output-dir DIR
                        Output directory for converted files
  -s SUFFIX, --suffix SUFFIX
                        Add suffix to output filenames (e.g., "_converted")
  --quality N           JPEG quality (1-100, default: 95)
  -f, --force           Overwrite existing output files

processing options:
  -r, --recursive       Process directories recursively
  -d, --delete-original Delete original HEIC files after successful conversion
  -j N, --jobs N        Number of parallel conversion jobs (default: 1)
  --dry-run             Show what would be converted without actually converting

display options:
  -v, --verbose         Increase verbosity (use -vv for debug output)
  -q, --quiet           Suppress all output except errors
  --progress            Show progress bar during batch conversion
  --no-color            Disable colored output

logging options:
  --log-file FILE       Write logs to file in addition to console
```

## Logging

The tool provides structured logging with different levels:
- **ERROR**: Only critical errors
- **WARNING**: Warnings and errors (default)
- **INFO**: General information about operations (`-v`)
- **DEBUG**: Detailed debugging information (`-vv`)

Log messages include timestamps and are color-coded for easy reading in the terminal.

## Safety Features

- **Dry Run Mode**: Test your command without making changes
- **No Overwrite by Default**: Skips existing files unless `-f` is specified
- **Detailed Error Reporting**: Clear messages for troubleshooting
- **Atomic Operations**: Each file is processed independently

## Performance

- **Parallel Processing**: Use `-j N` to process multiple files simultaneously
- **Progress Tracking**: Monitor conversion progress with `--progress`
- **Efficient File Discovery**: Fast glob-based file searching

## License

MIT License