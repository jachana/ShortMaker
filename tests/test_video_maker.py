import pytest
import numpy as np
from PIL import Image
import os
from src.main import create_frame, create_video_from_text

def test_create_frame_default_params():
    """Test create_frame with default parameters"""
    frame = create_frame("Test Text")
    
    # Check if frame is numpy array
    assert isinstance(frame, np.ndarray)
    
    # Check dimensions (default size is 640x480)
    assert frame.shape == (480, 640, 3)
    
    # Check if frame is not empty (all black)
    assert not np.all(frame == 0)

def test_create_frame_custom_size():
    """Test create_frame with custom size"""
    size = (800, 600)
    frame = create_frame("Test Text", size=size)
    
    assert frame.shape == (600, 800, 3)

def test_create_frame_custom_colors():
    """Test create_frame with custom background and text colors"""
    bg_color = (255, 0, 0)  # Red background
    text_color = 'blue'
    frame = create_frame("Test Text", bg_color=bg_color, text_color=text_color)
    
    # Check if background color is present
    assert np.any(frame[:, :, 0] == 255)  # Red channel should have 255 values

def test_create_frame_custom_position():
    """Test create_frame with custom text position"""
    text_position = (100, 100)
    frame = create_frame("Test Text", text_position=text_position)
    
    assert isinstance(frame, np.ndarray)

def test_create_video_basic():
    """Test basic video creation without background"""
    output_file = "test_output.mp4"
    test_text = "Test video creation"
    
    create_video_from_text(test_text, output_filename=output_file, duration=2)
    
    # Check if video file was created
    assert os.path.exists(output_file)
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)

def test_create_video_custom_params():
    """Test video creation with custom parameters"""
    output_file = "test_custom.mp4"
    test_text = "Custom test video"
    
    create_video_from_text(
        test_text,
        output_filename=output_file,
        duration=2,
        bg_color=(100, 100, 100),
        text_color='yellow',
        text_size=40
    )
    
    assert os.path.exists(output_file)
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)

# Negative test cases
def test_create_frame_empty_text():
    """Test create_frame with empty text"""
    frame = create_frame("")
    assert isinstance(frame, np.ndarray)

def test_create_frame_invalid_size():
    """Test create_frame with invalid size"""
    with pytest.raises(Exception):
        create_frame("Test", size=(0, 0))

# Test cleanup
def teardown_module(module):
    """Clean up any remaining test files"""
    test_files = ["test_output.mp4", "test_custom.mp4", "temp_audio.mp3"]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
