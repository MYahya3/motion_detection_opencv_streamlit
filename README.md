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
![Capture](https://github.com/MrYahya18/motion_deteection_opencv_streamlit/assets/88489038/ed0b45f1-890f-4a4f-acc2-0f91ac717fd2)

## Working Process

Here's an overview of the working process of the code:

1. Choose an Option from the sidebar e.g. Webcam or video to upload 
2. Click the start button to initialize the motion detector. 
4. Preprocess frames using background subtractor and foreground masking to create a reference model of the previous image.
5. If some pixel intensity value changes above the threshold, it obtains contours of the motion.
6. Draws a bounding box and write a text banner on the frame alerting motion detected.
7. Processed Video saved in Output Directory
8. Can also click the Stop button to stop the video
Please note that this README provides an overview of the motion detection script. For more details, refer to the code in the repository.
