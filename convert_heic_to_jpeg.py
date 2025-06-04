#!/usr/bin/env python3
import os
import sys
import argparse
import logging
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import colorlog

# Register HEIF opener with Pillow
register_heif_opener()

def setup_logging(verbosity=0, log_file=None):
    """Configure logging with colored output and appropriate level."""
    log_level = logging.WARNING
    if verbosity == 1:
        log_level = logging.INFO
    elif verbosity >= 2:
        log_level = logging.DEBUG
    
    # Create formatters
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)

def convert_heic_to_jpeg(input_path, output_path, quality=95, logger=None):
    """Convert a HEIC file to JPEG format."""
    if logger is None:
        logger = logging.getLogger(__name__)
    
    try:
        logger.debug(f"Opening HEIC file: {input_path}")
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (HEIC might have alpha channel)
            if img.mode != 'RGB':
                logger.debug(f"Converting image mode from {img.mode} to RGB")
                img = img.convert('RGB')
            
            # Save as JPEG
            logger.debug(f"Saving as JPEG with quality {quality}: {output_path}")
            img.save(output_path, 'JPEG', quality=quality)
            logger.info(f"Successfully converted: {input_path} -> {output_path}")
        
        return True, None
    except Exception as e:
        logger.error(f"Failed to convert {input_path}: {str(e)}")
        return False, str(e)

def find_heic_files(paths, recursive=False, logger=None):
    """Find all HEIC files in the given paths."""
    if logger is None:
        logger = logging.getLogger(__name__)
    
    heic_files = []
    extensions = ('.heic', '.heif', '.HEIC', '.HEIF')
    
    for path_str in paths:
        path = Path(path_str)
        
        if path.is_file():
            if path.suffix in extensions:
                heic_files.append(path)
                logger.debug(f"Found HEIC file: {path}")
        elif path.is_dir():
            if recursive:
                pattern = '**/*'
                logger.debug(f"Searching recursively in: {path}")
            else:
                pattern = '*'
                logger.debug(f"Searching in: {path}")
            
            for ext in extensions:
                found = list(path.glob(f"{pattern}{ext}"))
                heic_files.extend(found)
                if found:
                    logger.debug(f"Found {len(found)} {ext} files in {path}")
        else:
            logger.warning(f"Path does not exist: {path}")
    
    return sorted(set(heic_files))

def get_output_path(input_path, output_dir=None, suffix=''):
    """Generate output path for the converted file."""
    input_path = Path(input_path)
    base_name = input_path.stem
    
    if suffix:
        output_name = f"{base_name}{suffix}.jpg"
    else:
        output_name = f"{base_name}.jpg"
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / output_name
    else:
        return input_path.parent / output_name

def process_file(args, heic_file, logger):
    """Process a single HEIC file."""
    output_path = get_output_path(heic_file, args.output_dir, args.suffix)
    
    # Check if output already exists
    if output_path.exists() and not args.force:
        logger.warning(f"Output file already exists, skipping: {output_path}")
        return False, "Output file exists"
    
    if args.dry_run:
        logger.info(f"[DRY RUN] Would convert: {heic_file} -> {output_path}")
        if args.delete_original:
            logger.info(f"[DRY RUN] Would delete original: {heic_file}")
        return True, None
    
    # Perform conversion
    success, error = convert_heic_to_jpeg(heic_file, output_path, args.quality, logger)
    
    if success and args.delete_original:
        try:
            heic_file.unlink()
            logger.info(f"Deleted original file: {heic_file}")
        except Exception as e:
            logger.error(f"Failed to delete original file {heic_file}: {e}")
    
    return success, error

def main():
    parser = argparse.ArgumentParser(
        description='Convert HEIC/HEIF images to JPEG format with advanced options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Convert all HEIC files in current directory
  %(prog)s img1.heic img2.heic       # Convert specific files
  %(prog)s -r /path/to/photos        # Recursively convert all HEIC files
  %(prog)s -o converted/ --quality 85  # Output to directory with quality 85
  %(prog)s --dry-run -v              # Preview what would be converted
  %(prog)s -j 4 --progress           # Use 4 threads with progress bar
        """
    )
    
    # Input arguments
    parser.add_argument('paths', nargs='*', default=['.'],
                        help='Files or directories to process (default: current directory)')
    
    # Output options
    output_group = parser.add_argument_group('output options')
    output_group.add_argument('-o', '--output-dir', metavar='DIR',
                            help='Output directory for converted files')
    output_group.add_argument('-s', '--suffix', default='', metavar='SUFFIX',
                            help='Add suffix to output filenames (e.g., "_converted")')
    output_group.add_argument('--quality', type=int, default=95,
                            metavar='N', choices=range(1, 101),
                            help='JPEG quality (1-100, default: 95)')
    output_group.add_argument('-f', '--force', action='store_true',
                            help='Overwrite existing output files')
    
    # Processing options
    proc_group = parser.add_argument_group('processing options')
    proc_group.add_argument('-r', '--recursive', action='store_true',
                            help='Process directories recursively')
    proc_group.add_argument('-d', '--delete-original', action='store_true',
                            help='Delete original HEIC files after successful conversion')
    proc_group.add_argument('-j', '--jobs', type=int, default=1, metavar='N',
                            help='Number of parallel conversion jobs (default: 1)')
    proc_group.add_argument('--dry-run', action='store_true',
                            help='Show what would be converted without actually converting')
    
    # Display options
    display_group = parser.add_argument_group('display options')
    display_group.add_argument('-v', '--verbose', action='count', default=0,
                            help='Increase verbosity (use -vv for debug output)')
    display_group.add_argument('-q', '--quiet', action='store_true',
                            help='Suppress all output except errors')
    display_group.add_argument('--progress', action='store_true',
                            help='Show progress bar during batch conversion')
    display_group.add_argument('--no-color', action='store_true',
                            help='Disable colored output')
    
    # Logging options
    log_group = parser.add_argument_group('logging options')
    log_group.add_argument('--log-file', metavar='FILE',
                            help='Write logs to file in addition to console')
    
    args = parser.parse_args()
    
    # Handle quiet mode
    if args.quiet:
        args.verbose = -1
    
    # Disable color if requested
    if args.no_color:
        colorlog.disable_colors()
    
    # Setup logging
    logger = setup_logging(args.verbose, args.log_file)
    logger.debug(f"Command line arguments: {args}")
    
    # Find all HEIC files
    logger.info("Searching for HEIC files...")
    heic_files = find_heic_files(args.paths, args.recursive, logger)
    
    if not heic_files:
        logger.warning("No HEIC files found to convert.")
        return 1
    
    logger.info(f"Found {len(heic_files)} HEIC file(s) to convert")
    
    # Process files
    successful = 0
    failed = 0
    
    if args.jobs > 1:
        # Parallel processing
        logger.info(f"Processing files using {args.jobs} parallel jobs")
        
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(process_file, args, heic_file, logger): heic_file
                for heic_file in heic_files
            }
            
            # Process results with progress bar
            if args.progress and not args.quiet:
                futures = tqdm(as_completed(future_to_file), total=len(heic_files),
                             desc="Converting", unit="file")
            else:
                futures = as_completed(future_to_file)
            
            for future in futures:
                heic_file = future_to_file[future]
                try:
                    success, error = future.result()
                    if success:
                        successful += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Unexpected error processing {heic_file}: {e}")
                    failed += 1
    else:
        # Sequential processing
        if args.progress and not args.quiet:
            file_iterator = tqdm(heic_files, desc="Converting", unit="file")
        else:
            file_iterator = heic_files
        
        for heic_file in file_iterator:
            success, error = process_file(args, heic_file, logger)
            if success:
                successful += 1
            else:
                failed += 1
    
    # Summary
    logger.info(f"Conversion complete! Successfully converted: {successful}, Failed: {failed}")
    
    if args.dry_run:
        logger.info("This was a dry run - no files were actually converted")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())