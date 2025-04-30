import cv2
import os
import glob
import re

def create_video_from_frames(frames_dir, output_video_path, fps=30):
    """
    Creates a video from a series of annotated frames.
    
    Args:
        frames_dir (str): Directory containing the annotated frames
        output_video_path (str): Path for the output video file
        fps (int): Frames per second for the output video
    """
    # Get all annotated frame files
    frame_pattern = os.path.join(frames_dir, "annotated_frame_*.jpg")
    frame_files = sorted(glob.glob(frame_pattern), 
                         key=lambda x: int(re.search(r'annotated_frame_(\d+)', os.path.basename(x)).group(1)))
    
    if not frame_files:
        print(f"No annotated frames found in {frames_dir}")
        return False
    
    # Read the first frame to get dimensions
    first_frame = cv2.imread(frame_files[0])
    height, width, layers = first_frame.shape
    
    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID' if mp4v doesn't work
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    # Add each frame to the video
    total_frames = len(frame_files)
    print(f"Creating video from {total_frames} frames...")
    
    for i, frame_file in enumerate(frame_files):
        if i % 10 == 0:  # Progress update every 10 frames
            print(f"Processing frame {i+1}/{total_frames}")
        
        frame = cv2.imread(frame_file)
        video_writer.write(frame)
    
    # Release the video writer
    video_writer.release()
    print(f"Video saved to {output_video_path}")
    return True

# Example usage - add this to your main script
if __name__ == "__main__":
    # After running the head motion detection
    frames_dir = "head_motion_framesEDIT"  # Directory where annotated frames were saved
    output_video = "head_motion_highlights.mp4"
    create_video_from_frames(frames_dir, output_video, fps=15)  # Lower fps for slower playback