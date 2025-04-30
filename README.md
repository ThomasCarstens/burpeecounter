

# Activate a virtual environment to install Python packages.
python3 -m venv face_detection_venv
source face_detection_venv/bin/activate


# Let's say your requirements.txt file contains the following:
numpy==1.21.2
pandas==1.3.3

# To install these packages, run the following command in your terminal:
pip install -r requirements.txt
