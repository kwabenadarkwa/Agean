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
        "monospace": 0.6,
        "syntax_colors": 0.2,
        "structure": 0.0,  # REMOVED - too many false positives
        "line_numbers": 0.15,
        "dark_theme": 0.05,
    }

    FINAL_THRESHOLD = 0.5
    MIN_COLOR_RATIO = 0.05
    MAX_WIDTH_VARIANCE = 20