import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def generate_motion_graph(frames_dir='head_motion_frames', output_path='motion_detection_graph.png'):
    """
    Generates a graph showing frames where motion was detected based on saved annotated JPG frames.
    
    Args:
        frames_dir (str): Directory containing the annotated frames
        output_path (str): Path to save the output graph
    """
    # Check if directory exists
    if not os.path.exists(frames_dir):
        print(f"Error: Directory {frames_dir} does not exist.")
        return
    
    # Get all annotated frame files
    frame_files = [f for f in os.listdir(frames_dir) if f.startswith('annotated_frame_') and f.endswith('.jpg')]
    
    if not frame_files:
        print(f"No annotated frames found in {frames_dir}")
        return
    
    # Extract frame numbers using regex
    frame_numbers = []
    pattern = re.compile(r'annotated_frame_(\d+)\.jpg')
    
    for file in frame_files:
        match = pattern.match(file)
        if match:
            frame_numbers.append(int(match.group(1)))
    
    # Sort frame numbers
    frame_numbers.sort()
    
    if not frame_numbers:
        print("Could not extract any valid frame numbers.")
        return
    
    # Get the max frame number to determine video length
    max_frame = max(frame_numbers)
    
    # Create a binary array: 1 where motion was detected, 0 elsewhere
    motion_data = np.zeros(max_frame + 1)
    for frame in frame_numbers:
        motion_data[frame] = 1
    
    # Create the plot
    plt.figure(figsize=(15, 6))
    
    # Plot the motion detection events
    plt.stem(range(len(motion_data)), motion_data, markerfmt='ro', linefmt='r-', basefmt=' ')
    
    # Add horizontal bars for periods with motion
    motion_periods = []
    start = None
    
    for i, val in enumerate(motion_data):
        if val == 1 and start is None:
            start = i
        elif val == 0 and start is not None:
            motion_periods.append((start, i-1))
            start = None
    
    # Handle the case where the last period extends to the end
    if start is not None:
        motion_periods.append((start, len(motion_data)-1))
    
    # Plot horizontal bars for motion periods
    for start, end in motion_periods:
        plt.axvspan(start, end, alpha=0.2, color='red', linewidth=0.1)
    
    # Configure plot
    plt.title('Head Motion Detection Timeline')
    plt.xlabel('Frame Number')
    plt.ylabel('Motion Detected')
    
    # Set y-axis to only show 0 and 1
    plt.yticks([0, 1], ['No', 'Yes'])
    
    # Improve x-axis readability
    plt.gca().xaxis.set_major_locator(MaxNLocator(20))  # Show ~20 tick marks on x-axis
    
    # Add grid lines for better readability
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Add statistics
    total_frames = len(motion_data)
    motion_frames = sum(motion_data)
    percent_motion = (motion_frames / total_frames) * 100
    
    stats_text = f"Total Frames: {total_frames}\n"
    stats_text += f"Frames with Motion: {int(motion_frames)} ({percent_motion:.2f}%)"
    
    plt.figtext(0.02, 0.02, stats_text, fontsize=10)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(output_path, dpi=600)
    plt.close()
    
    print(f"Graph saved to {output_path}")
    
    # Optional: Return data for further analysis
    return {
        'frame_numbers': frame_numbers,
        'total_frames': total_frames,
        'motion_frames': int(motion_frames),
        'percent_motion': percent_motion,
        'motion_periods': motion_periods
    }

# Additional function to analyze motion patterns
def analyze_motion_patterns(motion_data):
    """
    Analyzes patterns in motion detection data.
    
    Args:
        motion_data (dict): Output from generate_motion_graph function
    
    Returns:
        dict: Analysis results
    """
    if not motion_data:
        return None
    
    motion_periods = motion_data['motion_periods']
    frame_numbers = motion_data['frame_numbers']
    
    # Calculate interval between motion events
    intervals = []
    for i in range(1, len(frame_numbers)):
        intervals.append(frame_numbers[i] - frame_numbers[i-1])
    
    # Calculate duration of motion periods
    durations = [end - start + 1 for start, end in motion_periods]
    
    # Prepare analysis results
    results = {
        'total_motion_events': len(motion_periods),
        'avg_motion_duration': np.mean(durations) if durations else 0,
        'max_motion_duration': max(durations) if durations else 0,
        'min_motion_duration': min(durations) if durations else 0,
        'avg_interval_between_motions': np.mean(intervals) if intervals else 0,
    }
    
    return results

# Example usage
if __name__ == "__main__":
    motion_data = generate_motion_graph(frames_dir='head_motion_framesEDIT', 
                                       output_path='/home/thermistor/Documents/felix_counter/counter_editedpics.png')
    
    if motion_data:
        analysis = analyze_motion_patterns(motion_data)
        if analysis:
            print("\nMotion Analysis:")
            print(f"Total motion events: {analysis['total_motion_events']}")
            print(f"Average motion duration: {analysis['avg_motion_duration']:.2f} frames")
            print(f"Maximum motion duration: {analysis['max_motion_duration']} frames")
            print(f"Minimum motion duration: {analysis['min_motion_duration']} frames")
            print(f"Average interval between motions: {analysis['avg_interval_between_motions']:.2f} frames")