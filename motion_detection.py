import numpy as np
import cv2
import streamlit as st
import tempfile

# To draw banner and write text on it.
def drawBannerText(frame, text, banner_height_percent = 0.08, font_scale = 0.8, text_color = (0, 255, 0),
                   font_thickness = 1):
    # Draw a black filled banner across the top of the image frame.
    # percent: set the banner height as a percentage of the frame height.
    banner_height = int(banner_height_percent * frame.shape[0])
    cv2.rectangle(frame, (0, 0), (int(frame.shape[1]*0.5), banner_height), (255, 255, 255), thickness = -1)

    # Draw text on banner.
    left_offset = 20
    location = (left_offset, int(10 + (banner_height_percent * frame.shape[0]) / 2))
    cv2.putText(frame, text, location, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color,
                font_thickness, cv2.LINE_AA)


def motionDetector(video_cap):

    frame_placeholder = st.empty()
    stop_button = st.sidebar.button('Stop Processing')

    if stop_button:
        st.stop()

    if not video_cap.isOpened():
        print('Unable to open video')
    # Get video frame width, height and fps
    frame_w = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_area = frame_w * frame_h

    # Parameters
    ksize = (3, 3)        # Kernel size for erosion.
    max_contours = 3      # Number of contours to use for rendering a bounding rectangle.
    frame_count = 0
    frame_start = 5      # To reduce initial False Positive skip starting few frames
    min_contour_area_thresh = 0.01 # Minimum fraction of frame required for maximum contour.
    # Colors  RGB values
    red = (0, 0, 255)
    yellow = (0, 255, 255)


    # To create frame background subtractor with history of 1500 to reduce False Positive
    bg_sub = cv2.createBackgroundSubtractorKNN(history=1500)

                                ### Process video frames ###
    while True:
        ret, frame = video_cap.read()
        frame_count += 1
        if frame is None:
            break

        # Stage 1: Create a foreground mask for the current frame.
        fg_mask = bg_sub.apply(frame)
        # Stage 2: Stage 1 + Erosion.
        fg_mask_erode = cv2.erode(fg_mask, np.ones(ksize, np.uint8))
        # Stage 3: Stage 2 + Contours.
        contours_erode, hierarchy = cv2.findContours(fg_mask_erode, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Stage 4 Draw Boxes on Top Contours
        if len(contours_erode) > 0 and frame_count > frame_start:
            # Sort contours based on area.
            contours_sorted = sorted(contours_erode, key=cv2.contourArea, reverse=True)
            for idx in range(min(max_contours, len(contours_sorted))):

                # Contour area of largest contour.
                contour_area_max = cv2.contourArea(contours_sorted[idx])

                # Compute fraction of total frame area occupied by largest contour.
                contour_frac = contour_area_max / frame_area

                # Confirm contour_frac is greater than min_contour_area_thresh threshold.
                if contour_frac > min_contour_area_thresh:
                    xc, yc, wc, hc = cv2.boundingRect(contours_sorted[idx])
                    x1 = xc
                    y1 = yc
                    x2 = xc + wc
                    y2 = yc + hc

                    # Draw bounding rectangle for top N contours on output frame.
                    cv2.rectangle(frame, (x1, y1), (x2, y2), yellow, thickness=2)
                    drawBannerText(frame, 'Motion Detected', text_color=red)

        # Convert the frame from BGR to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Display the frame using Streamlit's st.image
        frame_placeholder.image(frame, channels="RGB")

        # Break the loop if the 'q' key is pressed or the user clicks the "Stop" button
        cv2.waitKey(1)
        if stop_button:
            st.stop()
    cv2.releaseall()
    cv2.destroyAllWindows()

def main():
    st.title('Motion Detection using Streamlit')

    selected_options = ["None", "Use Webcam", "Upload Video"]

    selected_option = st.sidebar.selectbox("Choose an Option ", selected_options)
    if selected_option == "Use Webcam":
        vid = cv2.VideoCapture(0)
    elif selected_option == "Upload Video":
        video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", 'avi', 'asf', 'm4v'],
                                                     accept_multiple_files=True)
        tfflie = tempfile.NamedTemporaryFile(delete=False)
        print(video_file_buffer)
        if video_file_buffer:
            video_files = [file.name for file in video_file_buffer]
            video_files  = list(dict.fromkeys(video_files))
            video_choose = st.selectbox("Choose the Video ", video_files)
            temp_vid_index = video_files.index(video_choose)
            tfflie.write(video_file_buffer[temp_vid_index].read())
            vid = cv2.VideoCapture(tfflie.name)
    else:
        st.warning("Please choose a valid video from the list.")
        st.stop()

    start = st.sidebar.button("Start")
    if start:
        motionDetector(vid)
    else:
        pass

if __name__ == "__main__":
    main()
