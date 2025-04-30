import cv2
import numpy as np
import os

def detect_head_motion(video_path, threshold_x, y_min_ratio=0.33, y_max_ratio=0.66, 
                      output_dir='head_motion_frames', skip_frames=10):
    """
    Detects frames where motion occurs right of an x threshold AND within a specific y-range
    (second third of the frame height) to target head movements.
    
    Args:
        video_path (str): Path to the input video file
        threshold_x (int): X-coordinate threshold
        y_min_ratio (float): Ratio of frame height for min y
        y_max_ratio (float): Ratio of frame height for max y
        output_dir (str): Directory to save matching frames
        skip_frames (int): Number of frames to skip after finding a match
    
    Returns:
        list: Frame numbers where head motion was detected
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return []
    
    # Initialize background subtractor
    backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
    
    frame_count = 400
    matching_frames = []
    frames_to_skip = 0
    
    # Read first frame to get dimensions
    ret, frame = cap.read()
    if not ret:
        print("Error reading video")
        return []
    
    height, width = frame.shape[:2]
    
    # Calculate y range for head detection (second third of the frame)
    y_min = int(height * y_min_ratio)
    y_max = int(height * y_max_ratio)
    
    print(f"Frame dimensions: {width}x{height}")
    print(f"X threshold: {threshold_x}")
    print(f"Y range for head detection: {y_min} to {y_max}")
    
    # Reset video to beginning
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    while True:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        
        # Report progress for every 100 frames
        if frame_count % 100 == 0:
            print(f"Processing frame {frame_count}...")
        
        # Skip frames if needed
        if frames_to_skip > 0:
            frames_to_skip -= 1
            frame_count += 1
            continue
        
        # Apply background subtraction
        fgMask = backSub.apply(frame)
        
        # Apply morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
        fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
        
        # Extract the region of interest: right of x threshold and within y range
        roi = fgMask[y_min:y_max, threshold_x:]
        
        # Check if significant motion is detected in the ROI
        roi_sum = np.sum(roi)
        # if frame_count % 100 == 0:
        # print(f"Frame {frame_count}: Sum of motion in head ROI = {roi_sum}")
        
        if roi_sum > 5000:  # Adjust this threshold based on your video
            # Save this frame
            # frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
            # cv2.imwrite(frame_filename, frame)
            
            # Create annotated frame
            annotated_frame = frame.copy()
            
            # Draw threshold line
            cv2.line(annotated_frame, (threshold_x, 0), (threshold_x, height), (0, 255, 0), 2)
            
            # Draw horizontal lines showing y range
            cv2.line(annotated_frame, (0, y_min), (width, y_min), (0, 0, 255), 2)
            cv2.line(annotated_frame, (0, y_max), (width, y_max), (0, 0, 255), 2)
            
            # Highlight ROI area
            roi_overlay = annotated_frame.copy()
            roi_overlay[y_min:y_max, threshold_x:, 1] = 255  # Green tint for ROI
            overlay = cv2.addWeighted(annotated_frame, 0.7, roi_overlay, 0.3, 0)

            # Rotate the frames 90 degrees counterclockwise to correct orientation
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            rotated_annotated = cv2.rotate(overlay, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
            # Save rotated frames
            # frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
            # cv2.imwrite(frame_filename, rotated_frame)
            
            annotated_frame_filename = os.path.join(output_dir, f"annotated_frame_{frame_count:06d}.jpg")
            cv2.imwrite(annotated_frame_filename, rotated_annotated)
            
            matching_frames.append(frame_count)
            # print(f"Head movement detected in frame {frame_count}")
            
            # Set frames to skip
            frames_to_skip = skip_frames
        
        frame_count += 1
        
    # Release video capture
    cap.release()
    
    print(f"Processed {frame_count} frames, found {len(matching_frames)} frames with head movement.")
    return matching_frames

# Example usage
if __name__ == "__main__":
    video_path = "/home/thermistor/Downloads/GX010031.MP4"  # Your video path
    threshold_x = 1300  # Adjust based on your video
    matching_frames = detect_head_motion(video_path, threshold_x, 
                                        y_min_ratio=0.33, y_max_ratio=0.66,  # Second third of the frame
                                        skip_frames=10)
    print(f"Frames with head movement: {matching_frames}")