"""
Code frame filtering module for detecting and filtering code frames from video sequences.

This module provides functionality to identify frames containing code using various
detection methods including monospace text analysis, syntax highlighting detection,
and structural pattern recognition.
"""

from .config import CodeDetectionConfig
from .detectors import is_code_frame
from .rule_based_filter import RemoveNonCodeFramesRuleBased
from .model_based_filter import RemoveNonCodeFramesWithModel

__all__ = [
    "CodeDetectionConfig",
    "is_code_frame",
    "RemoveNonCodeFramesRuleBased",
    "RemoveNonCodeFramesWithModel",
]