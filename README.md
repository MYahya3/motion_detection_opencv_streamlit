# Motion Detection with OpenCv and Streamlit

This script detects motion in a video and highlights it with a bounding box and text alert. The purpose is to provide a demo of how we can use a motion detection system to detect motion in Security areas even in Homes and receive an alert when motion is detected.

## Configuration

1. Clone the repository:

```bash
git clone https://github.com/MrYahya18/motion_deteection_opencv_streamlit.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To access the motion detector, run the following command:

```bash
streamlit run ./motion_detection.py
```
![image](https://github.com/MrYahya18/motion_deteection_opencv_streamlit/assets/88489038/246d5538-46e4-4538-8efc-faf9cefbe864)


## Working Process

Here's an overview of the working process of the code:

1. The script takes the path of a folder containing .mp4 videos, e.g., `videos_folder/1.mp4`, `videos_folder/2.mp4`, etc.
2. Define the name of the videos in the selection box.
3. The selected video is initialized with OpenCV.
4. Preprocess frames using background subtractor and foreground masking to create a reference model of the previous image.
5. If some pixel intensity value changes above the threshold, it obtains contours of the motion.
6. Draws a bounding box and writes a text banner on the frame alerting motion detected.

Please note that this README provides an overview of the motion detection script. For more details, refer to the code in the repository.
