

# Burpee Counter

A Python-based tool for automatically detecting and counting headshots from workout videos.

## Overview

Felix needed to make sure he did 1000 burpees. I collected headshots in the top burpee position instead of verifying the full motion of each burpee. 

![Burpee Detection Results](counter_editedpics.png)

In this example there are 19 sets of 50 burpees. Each set is a large red line made up of 50 sublines (zoom in on top subsection to count them).

It works by:
1. Extracting frames from your video 
2. Analyzing the frames to detect your head position
3. Keeping only the frames with the head in the top position ([example](https://drive.google.com/file/d/1X-Tt01s4wq5E0Yd5OBaNq0yrPR0Uf4IO/view?usp=sharing))
4. Graphing these head frames over time so that you can count burpees within sets but also crosscheck any parasitic frames.


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

# Navigate to line 137 of counter.py and edit your video path in
137    video_path = "/home/User/... .MP4   
```
## Run Counter.py 
```python3 counter.py```
It takes 1h30 or so to extract frames.

## Manual pruning : removing frames where you are not doing burpees
Some headshots include rest periods etc.

## Graph the times of the frames with head visible
```python3 graph.py```
