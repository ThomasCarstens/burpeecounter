

# Burpee Counter

A Python-based tool for automatically detecting and counting burpees from workout videos.

## Overview

This project helps you analyze your workout videos to count burpees automatically. It works by:
1. Extracting frames from your video
2. Analyzing the frames to detect your position
3. Identifying burpee movements
4. Visualizing the results

![Burpee Detection Results](counter_editedpics.png)

19 sets of 50 burpees. The 50 in question can be examined by zooming on upper or lower parts of the graph.

## Setup Instructions

### 1. Create a Virtual Environment

```bash
# Install Python virtual environment package
sudo apt install python3.12-venv

# Create a virtual environment
python3 -m venv face_detection_venv

# Activate the virtual environment
source face_detection_venv/bin/activate

# install the required python packages
pip install -r requirements.txt
```


## Is the video stored on your PC? Edit counter.py 
```bash
137    video_path = "/home/User/... .MP4   "  # Your video path on line 137
```
## Run Counter.py 
```python3 counter.py```
It takes 1h30 or so to extract frames.

## Manual pruning : removing frames where you are not doing burpees

## Graph the times of the frames with head visible
```python3 graph.py```

![Burpee Detection Results](counter_editedpics.png)