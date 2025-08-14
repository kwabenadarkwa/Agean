"""
Core detection functions for identifying code frames in images.

This module contains all the computer vision algorithms used to detect
various characteristics of code frames including monospace text, syntax
highlighting, indentation patterns, line numbers, and dark themes.
"""

from pathlib import Path
from typing import Union

import cv2
import numpy as np

from .config import CodeDetectionConfig


def detect_monospace_text(image_path: Union[str, Path], config: type[CodeDetectionConfig] = CodeDetectionConfig) -> int:
    """
    Detect if image contains monospace text by analyzing character width consistency.

    The function converts the image to grayscale, applies binary thresholding, finds text contours,
    and measures their width variance. Low variance indicates uniform character widths typical of
    monospace fonts used in code editors and terminals.

    Args:
        image_path: Path to the image file.
        config: Configuration object with detection parameters.

    Returns:
        1 if monospace text detected (width variance < threshold), 0 otherwise.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text_contours = [
        c
        for c in contours
        if config.MIN_CONTOUR_AREA < cv2.contourArea(c) < config.MAX_CONTOUR_AREA
    ]

    if len(text_contours) < config.MIN_TEXT_CONTOURS:
        return 0

    widths = [cv2.boundingRect(c)[2] for c in text_contours]
    width_variance = np.var(widths)

    return 1 if width_variance < config.MAX_WIDTH_VARIANCE else 0


def detect_programming_colors(image_path: Union[str, Path], config: type[CodeDetectionConfig] = CodeDetectionConfig) -> int:
    """
    Detect syntax highlighting colors commonly used in code editors.

    Converts image to HSV color space and searches for specific color ranges
    (blue for keywords, green for strings, purple for types). Calculates the
    ratio of colored pixels to total pixels to determine if syntax highlighting
    is present.

    Args:
        image_path: Path to the image file.
        config: Configuration with color ranges and thresholds.

    Returns:
        1 if syntax highlighting colors detected (ratio > threshold), 0 otherwise.
    """
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


def detect_indentation_patterns(image_path: Union[str, Path], config: type[CodeDetectionConfig] = CodeDetectionConfig) -> int:
    """
    Detect code indentation patterns by finding vertical lines in the image.

    Uses Canny edge detection followed by Hough line transform to identify
    vertical lines that typically appear in code due to consistent indentation
    and block structure. Counts lines that are nearly vertical (within tolerance).

    Args:
        image_path: Path to the image file.
        config: Configuration with line detection parameters.

    Returns:
        1 if sufficient vertical lines detected (indicating code structure), 0 otherwise.
    """
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0

    edges = cv2.Canny(img, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=config.HOUGH_THRESHOLD)

    if lines is None:
        return 0

    vertical_lines = 0
    for line in lines:
        rho, theta = line[0]
        if abs(theta - np.pi / 2) < config.VERTICAL_ANGLE_TOLERANCE:
            vertical_lines += 1

    return 1 if vertical_lines > config.MIN_VERTICAL_LINES else 0


def detect_line_numbers(image_path: Union[str, Path], config: type[CodeDetectionConfig] = CodeDetectionConfig) -> int:
    """
    Detect line numbers in the left margin of code editors.

    Analyzes the leftmost region of the image for regularly spaced dark pixels
    that indicate line numbers. Creates a horizontal projection to find peaks
    (lines with text) and checks if their spacing is consistent, which is
    characteristic of sequential line numbering.

    Args:
        image_path: Path to the image file.
        config: Configuration with line number detection parameters.

    Returns:
        1 if consistent line number pattern detected, 0 otherwise.
    """
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0

    h, w = img.shape
    left_region = img[:, : int(w * config.LINE_NUMBER_REGION_WIDTH)]

    horizontal_projection = np.sum(left_region < 128, axis=1)

    peaks = []
    for i in range(1, len(horizontal_projection) - 1):
        if (
            horizontal_projection[i] > horizontal_projection[i - 1]
            and horizontal_projection[i] > horizontal_projection[i + 1]
            and horizontal_projection[i] > config.MIN_DARK_PIXELS_PER_LINE
        ):
            peaks.append(i)

    if len(peaks) < config.MIN_LINES_FOR_DETECTION:
        return 0

    spacings = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
    spacing_variance = np.var(spacings)

    return 1 if spacing_variance < config.MAX_SPACING_VARIANCE else 0


def detect_dark_background(image_path: Union[str, Path], config: type[CodeDetectionConfig] = CodeDetectionConfig) -> int:
    """
    Detect dark theme background commonly used in code editors.

    Converts image to grayscale and calculates the mean brightness across
    all pixels. Dark themes typically have low average brightness values,
    which helps distinguish code editors from bright web pages or documents.

    Args:
        image_path: Path to the image file.
        config: Configuration with brightness threshold.

    Returns:
        1 if dark theme detected (mean brightness < threshold), 0 otherwise.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)

    return 1 if mean_brightness < config.DARK_THEME_BRIGHTNESS_THRESHOLD else 0


def is_code_frame(image_path: Union[str, Path], config: type[CodeDetectionConfig] = CodeDetectionConfig, verbose: bool = False) -> bool:
    """
    Main function to detect if an image contains code.

    Runs all detection algorithms and combines their results using weighted scoring
    to determine if the image contains code. Each detection method contributes to
    a final score that is compared against a threshold.

    Args:
        image_path: Path to image file
        config: Configuration object with detection parameters
        verbose: If True, print detailed results

    Returns:
        True if image is detected as code frame, False otherwise
    """
    try:
        has_monospace = detect_monospace_text(image_path, config)
        has_syntax_colors = detect_programming_colors(image_path, config)
        has_code_structure = detect_indentation_patterns(image_path, config)
        has_line_numbers = detect_line_numbers(image_path, config)
        has_dark_theme = detect_dark_background(image_path, config)

        score = (
            has_monospace * config.WEIGHTS["monospace"]
            + has_syntax_colors * config.WEIGHTS["syntax_colors"]
            + has_code_structure * config.WEIGHTS["structure"]
            + has_line_numbers * config.WEIGHTS["line_numbers"]
            + has_dark_theme * config.WEIGHTS["dark_theme"]
        )

        is_code = score > config.FINAL_THRESHOLD

        if verbose:
            print(f"\n=== Code Detection Results for {Path(image_path).name} ===")
            print(
                f"Monospace text:     {'✓' if has_monospace else '✗'} (weight: {config.WEIGHTS['monospace']})"
            )
            print(
                f"Syntax colors:      {'✓' if has_syntax_colors else '✗'} (weight: {config.WEIGHTS['syntax_colors']})"
            )
            print(
                f"Code structure:     {'✓' if has_code_structure else '✗'} (weight: {config.WEIGHTS['structure']})"
            )
            print(
                f"Line numbers:       {'✓' if has_line_numbers else '✗'} (weight: {config.WEIGHTS['line_numbers']})"
            )
            print(
                f"Dark theme:         {'✓' if has_dark_theme else '✗'} (weight: {config.WEIGHTS['dark_theme']})"
            )
            print(f"\nFinal score:        {score:.3f}")
            print(f"Threshold:          {config.FINAL_THRESHOLD}")
            print(
                f"Result:             {'CODE FRAME' if is_code else 'NOT CODE FRAME'}"
            )

        return is_code

    except Exception as e:
        if verbose:
            print(f"Error processing {image_path}: {e}")
        return False
