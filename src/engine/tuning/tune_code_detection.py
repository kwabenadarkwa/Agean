#!/usr/bin/env python3
"""
Parameter tuning script for code detection.
Tests different parameter combinations to find optimal settings.
"""

import os
import glob
from pathlib import Path
from test_code_detection import CodeDetectionConfig, is_code_frame
import itertools


def get_sample_frames():
    """Get sample frames for testing."""
    # Python video frames (should be CODE)
    python_dir = "videos/Is \"finally\" Useless In Python?"
    python_frames = glob.glob(f"{python_dir}/*.jpg")[:20]  # First 20 frames
    
    # Ghana cooking video frames (should be NOT CODE) 
    ghana_dir = "videos/I MADE THIS AUTHENTIC GHANA 🇬🇭 GOAT LIGHT SOUP WITH FUFU IN UNDER AN HOUR. QUICK EASY & TASTY Try it"
    ghana_frames = glob.glob(f"{ghana_dir}/*.jpg")[:20]  # First 20 frames
    
    return python_frames, ghana_frames


def test_config_accuracy(config, code_frames, non_code_frames, verbose=False):
    """Test a configuration on sample frames and return accuracy metrics."""
    code_correct = 0
    non_code_correct = 0
    
    # Test code frames (should return True)
    for frame in code_frames:
        if os.path.exists(frame):
            try:
                result = is_code_frame(frame, config)
                if result:
                    code_correct += 1
                if verbose:
                    print(f"Code frame {Path(frame).name}: {'✓' if result else '✗'}")
            except Exception as e:
                if verbose:
                    print(f"Error testing {frame}: {e}")
    
    # Test non-code frames (should return False)
    for frame in non_code_frames:
        if os.path.exists(frame):
            try:
                result = is_code_frame(frame, config)
                if not result:
                    non_code_correct += 1
                if verbose:
                    print(f"Non-code frame {Path(frame).name}: {'✓' if not result else '✗'}")
            except Exception as e:
                if verbose:
                    print(f"Error testing {frame}: {e}")
    
    code_accuracy = code_correct / len(code_frames) if code_frames else 0
    non_code_accuracy = non_code_correct / len(non_code_frames) if non_code_frames else 0
    overall_accuracy = (code_correct + non_code_correct) / (len(code_frames) + len(non_code_frames))
    
    return {
        'code_accuracy': code_accuracy,
        'non_code_accuracy': non_code_accuracy, 
        'overall_accuracy': overall_accuracy,
        'code_correct': code_correct,
        'code_total': len(code_frames),
        'non_code_correct': non_code_correct,
        'non_code_total': len(non_code_frames)
    }


def create_config_variant(base_config, **overrides):
    """Create a config variant with specific parameter overrides."""
    class ConfigVariant(base_config):
        pass
    
    for key, value in overrides.items():
        if key == 'weights':
            ConfigVariant.WEIGHTS = value
        else:
            setattr(ConfigVariant, key.upper(), value)
    
    return ConfigVariant


def tune_single_parameters():
    """Tune individual parameters one at a time."""
    print("=== SINGLE PARAMETER TUNING ===\n")
    
    python_frames, ghana_frames = get_sample_frames()
    base_config = CodeDetectionConfig
    
    # Test baseline
    baseline_results = test_config_accuracy(base_config, python_frames, ghana_frames)
    print(f"BASELINE CONFIG:")
    print(f"  Code accuracy: {baseline_results['code_accuracy']:.1%} ({baseline_results['code_correct']}/{baseline_results['code_total']})")
    print(f"  Non-code accuracy: {baseline_results['non_code_accuracy']:.1%} ({baseline_results['non_code_correct']}/{baseline_results['non_code_total']})")
    print(f"  Overall accuracy: {baseline_results['overall_accuracy']:.1%}")
    print()
    
    # Test different final thresholds
    print("Testing FINAL_THRESHOLD values:")
    for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
        config = create_config_variant(base_config, final_threshold=threshold)
        results = test_config_accuracy(config, python_frames, ghana_frames)
        print(f"  {threshold:.1f}: Overall {results['overall_accuracy']:.1%} (Code: {results['code_accuracy']:.1%}, Non-code: {results['non_code_accuracy']:.1%})")
    print()
    
    # Test different color ratio thresholds
    print("Testing MIN_COLOR_RATIO values:")
    for ratio in [0.01, 0.02, 0.03, 0.05, 0.08, 0.1]:
        config = create_config_variant(base_config, min_color_ratio=ratio)
        results = test_config_accuracy(config, python_frames, ghana_frames)
        print(f"  {ratio:.2f}: Overall {results['overall_accuracy']:.1%} (Code: {results['code_accuracy']:.1%}, Non-code: {results['non_code_accuracy']:.1%})")
    print()
    
    # Test different width variance thresholds
    print("Testing MAX_WIDTH_VARIANCE values:")
    for variance in [10, 20, 30, 50, 100]:
        config = create_config_variant(base_config, max_width_variance=variance)
        results = test_config_accuracy(config, python_frames, ghana_frames)
        print(f"  {variance}: Overall {results['overall_accuracy']:.1%} (Code: {results['code_accuracy']:.1%}, Non-code: {results['non_code_accuracy']:.1%})")
    print()


def tune_weight_combinations():
    """Test different weight combinations."""
    print("=== WEIGHT COMBINATION TUNING ===\n")
    
    python_frames, ghana_frames = get_sample_frames()
    base_config = CodeDetectionConfig
    
    # Test different weight emphasis
    weight_configs = [
        ("Balanced", {'monospace': 0.25, 'syntax_colors': 0.25, 'structure': 0.2, 'line_numbers': 0.15, 'dark_theme': 0.15}),
        ("Color-focused", {'monospace': 0.15, 'syntax_colors': 0.4, 'structure': 0.15, 'line_numbers': 0.15, 'dark_theme': 0.15}),
        ("Monospace-focused", {'monospace': 0.4, 'syntax_colors': 0.2, 'structure': 0.15, 'line_numbers': 0.15, 'dark_theme': 0.1}),
        ("Structure-focused", {'monospace': 0.2, 'syntax_colors': 0.2, 'structure': 0.4, 'line_numbers': 0.1, 'dark_theme': 0.1}),
        ("Visual-only", {'monospace': 0.3, 'syntax_colors': 0.3, 'structure': 0.2, 'line_numbers': 0.0, 'dark_theme': 0.2}),
    ]
    
    for name, weights in weight_configs:
        config = create_config_variant(base_config, weights=weights)
        results = test_config_accuracy(config, python_frames, ghana_frames)
        print(f"{name:15}: Overall {results['overall_accuracy']:.1%} (Code: {results['code_accuracy']:.1%}, Non-code: {results['non_code_accuracy']:.1%})")
    print()


def find_best_combination():
    """Grid search for best parameter combination."""
    print("=== GRID SEARCH FOR BEST COMBINATION ===\n")
    
    python_frames, ghana_frames = get_sample_frames()
    base_config = CodeDetectionConfig
    
    # Define parameter ranges to test
    thresholds = [0.2, 0.3, 0.4]
    color_ratios = [0.02, 0.03, 0.05]
    width_variances = [20, 30, 50]
    
    best_accuracy = 0
    best_config = None
    best_params = None
    
    print("Testing parameter combinations...")
    total_combinations = len(thresholds) * len(color_ratios) * len(width_variances)
    current = 0
    
    for threshold, color_ratio, width_variance in itertools.product(thresholds, color_ratios, width_variances):
        current += 1
        config = create_config_variant(
            base_config,
            final_threshold=threshold,
            min_color_ratio=color_ratio,
            max_width_variance=width_variance
        )
        
        results = test_config_accuracy(config, python_frames, ghana_frames)
        
        if results['overall_accuracy'] > best_accuracy:
            best_accuracy = results['overall_accuracy']
            best_config = results
            best_params = {
                'final_threshold': threshold,
                'min_color_ratio': color_ratio,
                'max_width_variance': width_variance
            }
        
        print(f"  {current}/{total_combinations}: Threshold={threshold}, ColorRatio={color_ratio}, WidthVar={width_variance} -> {results['overall_accuracy']:.1%}")
    
    print(f"\nBEST CONFIGURATION FOUND:")
    print(f"  Parameters: {best_params}")
    print(f"  Code accuracy: {best_config['code_accuracy']:.1%} ({best_config['code_correct']}/{best_config['code_total']})")
    print(f"  Non-code accuracy: {best_config['non_code_accuracy']:.1%} ({best_config['non_code_correct']}/{best_config['non_code_total']})")
    print(f"  Overall accuracy: {best_config['overall_accuracy']:.1%}")
    
    return best_params, best_config


def generate_optimized_config(best_params):
    """Generate code for optimized configuration class."""
    print("\n=== OPTIMIZED CONFIGURATION CLASS ===\n")
    
    config_code = f'''
class OptimizedCodeDetectionConfig(CodeDetectionConfig):
    """Optimized configuration based on parameter tuning."""
    
    # Optimized parameters
    FINAL_THRESHOLD = {best_params['final_threshold']}
    MIN_COLOR_RATIO = {best_params['min_color_ratio']}
    MAX_WIDTH_VARIANCE = {best_params['max_width_variance']}
    
    # You can add more optimized parameters here based on results
'''
    
    print(config_code)
    print("Add this class to your test_code_detection.py file!")


def detailed_analysis():
    """Analyze specific frames that are failing."""
    print("=== DETAILED ANALYSIS OF FAILING FRAMES ===\n")
    
    python_frames, ghana_frames = get_sample_frames()
    base_config = CodeDetectionConfig
    
    print("Analyzing Python frames (should be CODE but detected as NOT CODE):")
    for i, frame in enumerate(python_frames[:5]):  # First 5 frames
        if os.path.exists(frame):
            print(f"\nFrame {i+1}: {Path(frame).name}")
            result = is_code_frame(frame, base_config, verbose=True)
    
    print("\n" + "="*60)
    print("Analyzing Ghana frames that were incorrectly detected as CODE:")
    
    # Find some false positives from Ghana video
    false_positives = []
    for frame in ghana_frames:
        if os.path.exists(frame):
            if is_code_frame(frame, base_config):
                false_positives.append(frame)
                if len(false_positives) >= 3:  # Just analyze first 3
                    break
    
    for i, frame in enumerate(false_positives):
        print(f"\nFalse Positive {i+1}: {Path(frame).name}")
        result = is_code_frame(frame, base_config, verbose=True)


def main():
    """Main tuning function."""
    print("CODE DETECTION PARAMETER TUNING")
    print("="*50)
    
    # Check if sample frames exist
    python_frames, ghana_frames = get_sample_frames()
    
    if not python_frames:
        print("Error: No Python video frames found!")
        return
    if not ghana_frames:
        print("Error: No Ghana video frames found!")
        return
    
    print(f"Found {len(python_frames)} Python frames and {len(ghana_frames)} Ghana frames for testing.\n")
    
    # Run different tuning approaches
    tune_single_parameters()
    tune_weight_combinations()
    best_params, best_config = find_best_combination()
    generate_optimized_config(best_params)
    
    print("\n" + "="*60)
    print("DETAILED ANALYSIS")
    print("="*60)
    detailed_analysis()


if __name__ == "__main__":
    main()