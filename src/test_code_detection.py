#!/usr/bin/env python3
"""
Standalone script to test code frame detection on individual images.
Usage: python test_code_detection.py <image_path>
"""

import sys
import cv2
import numpy as np
from pathlib import Path


class CodeDetectionConfig:
    """Configuration class for code detection parameters."""
    
    # Monospace detection
    MIN_CONTOUR_AREA = 5
    MAX_CONTOUR_AREA = 500
    MAX_WIDTH_VARIANCE = 20
    MIN_TEXT_CONTOURS = 10
    
    # Syntax colors
    MIN_COLOR_RATIO = 0.05
    BLUE_RANGE = [(100, 50, 50), (130, 255, 255)]
    GREEN_RANGE = [(40, 50, 50), (80, 255, 255)]
    PURPLE_RANGE = [(130, 50, 50), (160, 255, 255)]
    
    # Structure detection
    HOUGH_THRESHOLD = 100
    MIN_VERTICAL_LINES = 5
    VERTICAL_ANGLE_TOLERANCE = 0.1
    
    # Line numbers
    LINE_NUMBER_REGION_WIDTH = 0.1
    MAX_SPACING_VARIANCE = 100
    MIN_DARK_PIXELS_PER_LINE = 5
    MIN_LINES_FOR_DETECTION = 3
    
    # Dark theme
    DARK_THEME_BRIGHTNESS_THRESHOLD = 80
    
    # Final scoring
    WEIGHTS = {
        'monospace': 0.25,
        'syntax_colors': 0.25,
        'structure': 0.2,
        'line_numbers': 0.15,
        'dark_theme': 0.15
    }
    FINAL_THRESHOLD = 0.4


class OptimizedCodeDetectionConfig(CodeDetectionConfig):
    """Rebalanced configuration - prioritizes monospace detection."""
    
    # Conservative threshold
    FINAL_THRESHOLD = 0.5
    MIN_COLOR_RATIO = 0.05
    MAX_WIDTH_VARIANCE = 20
    
    # Rebalanced weights - monospace is most reliable indicator
    WEIGHTS = {
        'monospace': 0.6,        # INCREASED - most reliable code indicator
        'syntax_colors': 0.2,    # DECREASED - nice to have, not essential
        'structure': 0.0,        # REMOVED - too many false positives
        'line_numbers': 0.15,    # Keep - very specific to code editors
        'dark_theme': 0.05       # Minimal - too common in all videos
    }


class RefinedCodeDetectionConfig(CodeDetectionConfig):
    """Refined configuration to reduce false positives while maintaining good code detection."""
    
    # Balanced threshold - not too strict, not too lenient
    FINAL_THRESHOLD = 0.4
    
    # More specific color detection for programming
    MIN_COLOR_RATIO = 0.03
    
    # Relaxed monospace requirements (since it's often failing on real code)
    MAX_WIDTH_VARIANCE = 40
    MIN_TEXT_CONTOURS = 8
    
    # Moderate structure detection
    MIN_VERTICAL_LINES = 4
    HOUGH_THRESHOLD = 70
    
    # Relaxed line number detection
    MAX_SPACING_VARIANCE = 120
    MIN_LINES_FOR_DETECTION = 3
    
    # More specific programming color ranges (tighter HSV ranges)
    BLUE_RANGE = [(110, 100, 100), (125, 255, 255)]    # More specific blue for keywords
    GREEN_RANGE = [(50, 80, 80), (70, 255, 255)]       # More specific green for strings
    PURPLE_RANGE = [(135, 80, 80), (155, 255, 255)]    # More specific purple for types
    
    # Require multiple features to be present (higher threshold + balanced weights)
    WEIGHTS = {
        'monospace': 0.3,        # Increase - important for code
        'syntax_colors': 0.3,    # Increase - but with stricter detection
        'structure': 0.2,        # Reduce - too many false positives
        'line_numbers': 0.15,    # Moderate - helpful when present
        'dark_theme': 0.05       # Minimize - too common in all videos
    }


def detect_monospace_text(image_path, config=CodeDetectionConfig):
    """Detect if image contains monospace text."""
    img = cv2.imread(str(image_path))
    if img is None:
        return 0
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_contours = [c for c in contours 
                    if config.MIN_CONTOUR_AREA < cv2.contourArea(c) < config.MAX_CONTOUR_AREA]
    
    if len(text_contours) < config.MIN_TEXT_CONTOURS:
        return 0
    
    widths = [cv2.boundingRect(c)[2] for c in text_contours]
    width_variance = np.var(widths)
    
    return 1 if width_variance < config.MAX_WIDTH_VARIANCE else 0


def detect_programming_colors(image_path, config=CodeDetectionConfig):
    """Detect syntax highlighting colors."""
    img = cv2.imread(str(image_path))
    if img is None:
        return 0
        
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    total_pixels = img.shape[0] * img.shape[1]
    color_pixels = 0
    
    color_ranges = [config.BLUE_RANGE, config.GREEN_RANGE, config.PURPLE_RANGE]
    
    for lower, upper in color_ranges:
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        color_pixels += cv2.countNonZero(mask)
    
    color_ratio = color_pixels / total_pixels
    return 1 if color_ratio > config.MIN_COLOR_RATIO else 0


def detect_indentation_patterns(image_path, config=CodeDetectionConfig):
    """Detect code indentation patterns."""
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0
    
    edges = cv2.Canny(img, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=config.HOUGH_THRESHOLD)
    
    if lines is None:
        return 0
    
    vertical_lines = 0
    for line in lines:
        rho, theta = line[0]
        if abs(theta - np.pi/2) < config.VERTICAL_ANGLE_TOLERANCE:
            vertical_lines += 1
    
    return 1 if vertical_lines > config.MIN_VERTICAL_LINES else 0


def detect_line_numbers(image_path, config=CodeDetectionConfig):
    """Detect line numbers in left margin."""
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0
        
    h, w = img.shape
    left_region = img[:, :int(w * config.LINE_NUMBER_REGION_WIDTH)]
    
    horizontal_projection = np.sum(left_region < 128, axis=1)
    
    peaks = []
    for i in range(1, len(horizontal_projection) - 1):
        if (horizontal_projection[i] > horizontal_projection[i-1] and 
            horizontal_projection[i] > horizontal_projection[i+1] and
            horizontal_projection[i] > config.MIN_DARK_PIXELS_PER_LINE):
            peaks.append(i)
    
    if len(peaks) < config.MIN_LINES_FOR_DETECTION:
        return 0
    
    spacings = [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)]
    spacing_variance = np.var(spacings)
    
    return 1 if spacing_variance < config.MAX_SPACING_VARIANCE else 0


def detect_dark_background(image_path, config=CodeDetectionConfig):
    """Detect dark theme background."""
    img = cv2.imread(str(image_path))
    if img is None:
        return 0
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    
    return 1 if mean_brightness < config.DARK_THEME_BRIGHTNESS_THRESHOLD else 0


def is_code_frame(image_path, config=CodeDetectionConfig, verbose=False):
    """
    Main function to detect if an image contains code.
    
    Args:
        image_path: Path to image file
        config: Configuration object with detection parameters
        verbose: If True, print detailed results
    
    Returns:
        bool: True if image is detected as code frame
    """
    try:
        # Run all detection functions
        has_monospace = detect_monospace_text(image_path, config)
        has_syntax_colors = detect_programming_colors(image_path, config)
        has_code_structure = detect_indentation_patterns(image_path, config)
        has_line_numbers = detect_line_numbers(image_path, config)
        has_dark_theme = detect_dark_background(image_path, config)
        
        # Calculate weighted score
        score = (has_monospace * config.WEIGHTS['monospace'] + 
                has_syntax_colors * config.WEIGHTS['syntax_colors'] +
                has_code_structure * config.WEIGHTS['structure'] +
                has_line_numbers * config.WEIGHTS['line_numbers'] +
                has_dark_theme * config.WEIGHTS['dark_theme'])
        
        is_code = score > config.FINAL_THRESHOLD
        
        if verbose:
            print(f"\n=== Code Detection Results for {Path(image_path).name} ===")
            print(f"Monospace text:     {'✓' if has_monospace else '✗'} (weight: {config.WEIGHTS['monospace']})")
            print(f"Syntax colors:      {'✓' if has_syntax_colors else '✗'} (weight: {config.WEIGHTS['syntax_colors']})")
            print(f"Code structure:     {'✓' if has_code_structure else '✗'} (weight: {config.WEIGHTS['structure']})")
            print(f"Line numbers:       {'✓' if has_line_numbers else '✗'} (weight: {config.WEIGHTS['line_numbers']})")
            print(f"Dark theme:         {'✓' if has_dark_theme else '✗'} (weight: {config.WEIGHTS['dark_theme']})")
            print(f"\nFinal score:        {score:.3f}")
            print(f"Threshold:          {config.FINAL_THRESHOLD}")
            print(f"Result:             {'CODE FRAME' if is_code else 'NOT CODE FRAME'}")
        
        return is_code
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


def main():
    """Command line interface for testing individual frames."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python test_code_detection.py <image_path> [--config]")
        print("Configs: --optimized, --refined")
        print("Example: python test_code_detection.py frame1.jpg")
        print("Example: python test_code_detection.py frame1.jpg --optimized")
        print("Example: python test_code_detection.py frame1.jpg --refined")
        sys.exit(1)
    
    image_path = sys.argv[1]
    config_flag = sys.argv[2] if len(sys.argv) == 3 else None
    
    if not Path(image_path).exists():
        print(f"Error: File '{image_path}' not found")
        sys.exit(1)
    
    # Choose configuration
    if config_flag == "--optimized":
        config = OptimizedCodeDetectionConfig
        config_name = "OPTIMIZED"
    elif config_flag == "--refined":
        config = RefinedCodeDetectionConfig
        config_name = "REFINED"
    else:
        config = CodeDetectionConfig
        config_name = "DEFAULT"
    
    print(f"Using {config_name} configuration")
    result = is_code_frame(image_path, config, verbose=True)
    
    print(f"\n{'='*50}")
    print(f"FINAL RESULT ({config_name}): {'CODE FRAME' if result else 'NOT CODE FRAME'}")
    print(f"{'='*50}")
    
    # Show comparison with other configs
    if config_name != "DEFAULT":
        print(f"\nFor comparison with DEFAULT config:")
        default_result = is_code_frame(image_path, CodeDetectionConfig, verbose=False)
        print(f"DEFAULT result: {'CODE FRAME' if default_result else 'NOT CODE FRAME'}")
    
    if config_name != "REFINED":
        print(f"For comparison with REFINED config:")
        refined_result = is_code_frame(image_path, RefinedCodeDetectionConfig, verbose=False)
        print(f"REFINED result: {'CODE FRAME' if refined_result else 'NOT CODE FRAME'}")


if __name__ == "__main__":
    main()